import pathlib

from PIL import Image, ExifTags
from pillow_heif import register_heif_opener

register_heif_opener()

src_dir = pathlib.Path("/mnt/c/Users/sebas/Dropbox/finished_miniatures")
dst_dir = pathlib.Path("img")


def main():
    format = "jpeg"

    fnames = []
    for p in src_dir.glob("*"):
        src_image = Image.open(p)
        exif_datetime = src_image.getexif()[ExifTags.Base.DateTime]
        fname = f"{exif_datetime.split(' ')[0].replace(':', '')}.{format}"

        if src_image.size[0] != src_image.size[1]:
            src_image = square_image(src_image)

        src_image.resize(size=(800, 800)).save(dst_dir / fname, format=format)
        src_image.thumbnail((200, 200))
        src_image.save(dst_dir / f"{fname}.thumbnail", format=format)
        fnames.append(fname)

    grid = Grid(ncols=4, data=sorted(fnames, reverse=True))
    print(grid.html(id="gallery-2023"))


def square_image(src_image):
    width, height = src_image.size
    newsize = max(height, width)
    new = Image.new(src_image.mode, size=(newsize, newsize))

    if width > height:
        new.paste(src_image, box=(0, int((newsize - height) / 2)))

    if width < height:
        new.paste(src_image, box=(int((newsize - width) / 2), 0))

    return new


class Grid:
    def __init__(self, ncols, data=None):
        self.ncols = ncols
        self.columns = [list() for _ in range(ncols)]
        self.nextcolumn = 0

        if data is not None:
            for d in data:
                self.insert(d)

    def insert(self, value):
        self.columns[self.nextcolumn].append(value)
        self.nextcolumn = (self.nextcolumn + 1) % self.ncols

    def html(self, id=None):
        lines = ['<div class="row">' if id is None else f'<div class="row" id="{id}">']

        for column in self.columns:
            lines.append('<div class="column">')
            for fname in column:
                lines.append(
                    f"<a href='img/{fname}'><img src='img/{fname}.thumbnail'></a>"
                )
            lines.append("</div>")
        lines.append("</div>")
        return "\n".join(lines)


if __name__ == "__main__":
    main()
