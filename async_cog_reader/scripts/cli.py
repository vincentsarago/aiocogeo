import asyncio
from functools import wraps

import typer

from async_cog_reader import COGReader

app = typer.Typer()

def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper

def _make_bold(s, **kwargs):
    return typer.style(s, bold=True, **kwargs)

def _create_ifd_table(ifds, start="\t"):
    table = f"{start}{_make_bold('Id', underline=True):<20}{_make_bold('Size', underline=True):<27}{_make_bold('TileSize', underline=True):<30}"
    for idx, ifd in enumerate(ifds):
        size = f"{ifd.ImageWidth.value}x{ifd.ImageHeight.value}"
        tile_size = f"{ifd.TileWidth.value}x{ifd.TileHeight.value}"
        table += f"\n\t\t{idx:<8}{size:<15}{tile_size:<30}"
    return table

@app.command()
@coro
async def info(filepath: str):
    sep = 25
    async with COGReader(filepath) as cog:
        profile = cog.profile
        typer.echo(
        f"""
        {_make_bold("FILE INFO:", underline=True)} {_make_bold(filepath)}

          {_make_bold("PROFILE")}
            {_make_bold("Width:"):<{sep}} {profile['width']}
            {_make_bold("Height:"):<{sep}} {profile['height']}
            {_make_bold("Bands:"):<{sep}} {profile['count']}
            {_make_bold("Dtype:"):<{sep}} {profile['dtype']}
            {_make_bold("Crs:"):<{sep}} {profile['crs']}
            {_make_bold("Origin:"):<{sep}} ({profile['transform'].c}, {profile['transform'].f})
            {_make_bold("Resolution:"):<{sep}} ({profile['transform'].a}, {profile['transform'].e})
            {_make_bold("BoundingBox:"):<{sep}} {cog.bounds}
            {_make_bold("Compression:"):<{sep}} {cog.ifds[0].compression}
            {_make_bold("Internal mask:"):<{sep}} {cog.is_masked}
        """
        )
        typer.echo(f"""\t  {_make_bold("IFD")}
            {_create_ifd_table(cog.ifds)}
        """)
        if cog.is_masked:
            typer.echo(f"""\t  {_make_bold("MASK IFD")}
                {_create_ifd_table(cog.mask_ifds, start="")}
            """)

@app.command()
@coro
async def tms(filepath: str):
    typer.echo("this isn't done yet")