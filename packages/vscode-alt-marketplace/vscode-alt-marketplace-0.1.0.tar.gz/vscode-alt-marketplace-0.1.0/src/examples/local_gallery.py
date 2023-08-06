from pathlib import Path
from typing import Dict, Literal, OrderedDict
from flask import Blueprint, Flask, render_template_string, request, abort

from ..components import Gallery, LocalGallerySrc
from ..models.gallery import (
    VSCODE_INSTALLATION_TARGET,
    AssetType,
    FilterType,
    GalleryFlags,
)
from ..utils.extension import get_version_asset, get_version, get_version_asset_uri
from ..utils.flask import render_asset, debug_run
from ..utils.matching import simple_query

from ..blueprints import (
    generate_asset_uri,
    generate_assets_blueprint,
    generate_gallery_blueprint,
)

TEMPLATES = (Path(__file__).parent / "templates").resolve()

app = Flask(__name__)

# To implement later
# https://update.code.visualstudio.com/commit:${commit_sha}/server-linux-x64/stable


gallery = Gallery(
    LocalGallerySrc(
        "private",
        asset_uri=lambda filepath, type, ext, ver: generate_asset_uri(filepath),
    )
)


gallery_bp = generate_gallery_blueprint(gallery)
assets_bp = generate_assets_blueprint(gallery.asset_src)

web_bp = Blueprint("web", "web")


@web_bp.route("/items")
def items():
    itemName = request.args.get("itemName", type=str)
    ext = gallery.exts_src.get_extension(itemName)

    if not ext:
        abort(404)
    ver = get_version(ext, None)
    if not ver:
        abort(404)

    vsix = get_version_asset(ver, AssetType.VSIX)
    tabs: Dict[str, tuple[str, str]] = OrderedDict()
    tabs[AssetType.Details.name] = "Overview", render_asset(
        *gallery.asset_src.get_asset(vsix, AssetType.Details)
    )
    tabs[AssetType.Changelog.name] = "Change Log", render_asset(
        *gallery.asset_src.get_asset(vsix, AssetType.Changelog)
    )

    return render_template_string(
        (TEMPLATES / "item.html.j2").read_text(), tabs=tabs, ext=ext, ver=ver
    )


@web_bp.route("/")
def landing():
    query = simple_query(
        request.args.get("search_text", type=str)
        or [
            {"filterType": FilterType.Target, "value": VSCODE_INSTALLATION_TARGET},
            {
                "filterType": FilterType.ExcludeWithFlags,
                "value": GalleryFlags.Unpublished,
            },
        ],
        flags=GalleryFlags.IncludeAssetUri
        | GalleryFlags.IncludeFiles
        | GalleryFlags.IncludeLatestVersionOnly,
    )
    resp = gallery.extension_query(query)
    return render_template_string(
        (TEMPLATES / "landing.html.j2").read_text(),
        exts=resp["results"][0]["extensions"],
    )


app.register_blueprint(assets_bp, url_prefix="/assets")
app.register_blueprint(gallery_bp, url_prefix="/_apis/public/gallery")
app.register_blueprint(web_bp)


app.jinja_env.globals.update(get_asset_uri=get_version_asset_uri, AssetType=AssetType)
