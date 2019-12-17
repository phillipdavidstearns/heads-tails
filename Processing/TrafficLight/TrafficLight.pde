String URL = "http://207.251.86.238/cctv994.jpg";
boolean drawLine = true;
boolean drawArea = true;
boolean update = false;
PImage traffic;
PImage buffer;
int interval = 2;
int x1=0, x2=0, y1=0, y2=0;

float hue=0;
float sat=0;
float val=0;
float lastHue=0;
float lastSat=0;
float lastVal=0;
color lastAverage=0;

Area a;

ArrayList<Area> areas = new ArrayList<Area>();

void setup()
{
  a = new Area(0, 0, 0, 0);
  size(10, 10);
  frameRate(30);
  background(0);
}

void draw()
{ 

  //String imageName = "NYDOT-" + year()+"_"+month()+"_"+day()+"_"+hour()+"_"+minute()+"_"+second()+".jpg";
  //traffic = downloadImage(imageName, URL);

  if (second() % interval == 0 && !update) {
    //println(keyPressed+"keyCode: "+keyCode);
    update = true;
    traffic = getImage(URL);
    if (traffic!=null) {
      buffer=traffic;
      image(traffic, 0, 0);
      if (traffic.width > 0 && traffic.height > 0) {
        traffic.resize(traffic.width*6, traffic.height*6);
        surface.setSize(traffic.width, traffic.height);
        color average = averageColor(buffer);
        hue=hue(average);
        sat=saturation(average);
        val=brightness(average);
        if (sat != 0 && hue != 0) {
          float dhue=hue-lastHue;
          float dsat=sat-lastSat;
          float dval=val-lastVal;
          println("red: "+red(average)+", green: "+green(average)+", blue: "+blue(average)+"hue: "+hue+", sat: "+sat+", val: "+val+" dhue: "+dhue+", dsat: "+dsat+", dval: "+dval);
          if ((dhue<-8 && dsat>10) || dval>15) println("possible red light");
          if ((dhue>8 && dsat<-10) || dval<-15) println("possible green light");
          lastHue=hue;
          lastSat=sat;
          lastVal=val;
        }
      }
    }
  } else if (update && second() % interval != 0 ) {
    update = false;
  }
  if (buffer!=null)image(buffer, 0, 0);
  if (drawLine) renderLines();
  if (drawArea) renderAreas();
}

void renderAreas() {
  for (Area a : areas) {
    a.render();
  }
}

color averageColor(PImage _img) {
  int r=0, g=0, b=0, count=0;
  if (areas.size() !=0) {
    for (Area a : areas) {
      color temp = a.average(_img);
      r+=temp >> 16 & 0xFF;
      g+=temp >> 8 & 0xFF;
      b+=temp & 0xFF;
      count++;
    }
    return color(r/count, g/count, b/count);
  } else {
    return color(0, 0, 0, 0);
  }
}


PImage redChannel(PImage _img) {
  _img.loadPixels();
  for (int i = 0; i < _img.pixels.length; i++) {
    _img.pixels[i] = color(_img.pixels[i] >> 16 & 0xFF);
  }
  _img.updatePixels();
  return _img;
}

PImage downloadImage(String fileName, String url) {

  PImage img = loadImage(url);
  if (img != null)
  {
    img.save(fileName); // Cache of the file
  } else
  {
    println("Unable to load the image from " + url);
    exit();
  }

  return img;
}

PImage getImage(String url)
{
  PImage img = null;
  img = loadImage(url);
  if (img == null) println("something went wrong");
  return img;
}

void renderLines() {
  stroke(color(255, 255, 255, 127));
  line(mouseX, 0, mouseX, height);
  line(0, mouseY, width, mouseY);
}

void mousePressed() {
  x1=mouseX;
  y1=mouseY;
}

void mouseDragged() {

  for (Area a : areas) {
    if (a.mouseOver() && !keyPressed) {
      a.x1+=mouseX-pmouseX;
      a.y1+=mouseY-pmouseY;
      a.x2+=mouseX-pmouseX;
      a.y2+=mouseY-pmouseY;
    }
  }
}

void mouseReleased() {
  x2=mouseX;
  y2=mouseY;

  //add an area
  if (keyPressed && keyCode == SHIFT) {
    areas.add(new Area(x1, y1, x2, y2));
  }
  //remove an area
  if (keyPressed && keyCode == ALT) {
    for (int i = areas.size() - 1; i >=0; i--) {
      Area a = areas.get(i);
      if (a.mouseOver())areas.remove(i);
    }
  }
}