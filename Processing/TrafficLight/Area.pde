class Area {
  int x1, x2, y1, y2;
  color f = color(255), s=color(255);

  Area(int _x1, int _y1, int _x2, int _y2) {
    if (_x1<=_x2 && _y1<=_y2) {
      x1=_x1;
      x2=_x2;
      y1=_y1;
      y2=_y2;
    } else if (_x1<=_x2 && _y1>=_y2) {
      x1=_x1;
      x2=_x2;
      y1=_y2;
      y2=_y1;
    } else if (_x1>=_x2 && _y1>=_y2) {
      x1=_x2;
      x2=_x1;
      y1=_y2;
      y2=_y1;
    } else if (_x1>=_x2 && _y1<=_y2) {
      x1=_x2;
      x2=_x1;
      y1=_y1;
      y2=_y2;
    }
  }

  void render() {

    if ( mouseOver()) {
      fill(color(255, 255, 255, 63));
      //fill(average());
    } else {
      noFill();
    }

    stroke(s);
    rectMode(CORNERS);
    rect(x1, y1, x2, y2);
  }

  boolean mouseOver() {
    return mouseX >= x1 && mouseX <= x2 && mouseY >= y1 && mouseY <= y2;
  }

  color average() {

    int r=0, g=0, b=0, count=0;

    loadPixels();
    for (int x = x1; x < x2; x++) {
      for (int y = y1; y < y2; y++) {
        color pixel = pixels[y*width+x];
        r+=pixel >> 16 & 0xFF;
        g+=pixel >> 8 & 0xFF;
        b+=pixel & 0xFF;
        count++;
      }
    }
    return color(r/count, g/count, b/count);
  }

  color average(PImage img) {
    if (img != null) {
      int r=0, g=0, b=0, count=0;

      img.loadPixels();
      for (int x = x1; x < x2; x++) {
        for (int y = y1; y < y2; y++) {
          color pixel = img.pixels[y*img.width+x];
          r+=pixel >> 16 & 0xFF;
          g+=pixel >> 8 & 0xFF;
          b+=pixel & 0xFF;
          count++;
        }
      }
      return color(r/count, g/count, b/count);
    } else {
      return color(0);
    }
  }
}