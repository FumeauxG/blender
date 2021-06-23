#include <stdio.h>
#include <math.h>

void select_faces(int *ptr, int max, int maxMold, float *normalX, float *normalY, float *normalZ, float maxAngle, float vecDirX, float vecDirY, float vecDirZ, int *faces, float *point1X, float *point1Y, float *point2X, float *point2Y, float *point3X, float *point3Y, float *point1Z, float *point2Z, float *point3Z);
int point_inside_trigon(float sx, float sy, float ax, float ay, float bx, float by, float cx, float cy);

void select_faces(int *ptr, int max, int maxMold, float *normalX, float *normalY, float *normalZ, float maxAngle, float vecDirX, float vecDirY, float vecDirZ, int *faces, float *point1X, float *point1Y, float *point2X, float *point2Y, float *point3X, float *point3Y, float *point1Z, float *point2Z, float *point3Z)
{
    int i;
    int j;
    int k = 0;
    float dot;
    float lenSq1;
    float lenSq2;
    float angle;
    float x2 = vecDirX;
    float y2 = vecDirY;
    float z2 = vecDirZ;
    
    float triangleCenterX;
    float triangleCenterY;
    float triangleCenterZ;
    float triangleCenterZ2;
    
    float flagBreak = 0;

    for (i = 0; i < max; i++) 
    {
      //printf("%i\n", ptr[i]);

      dot = normalX[i]*x2 + normalY[i]*y2 + normalZ[i]*z2;    //between [x1, y1, z1] and [x2, y2, z2]
      lenSq1 = normalX[i]*normalX[i] + normalY[i]*normalY[i] + normalZ[i]*normalZ[i];
      lenSq2 = x2*x2 + y2*y2 + z2*z2;
      angle = acos(dot/sqrt(lenSq1 * lenSq2));

      if((angle*180/M_PI) < maxAngle || ((dot > 0.9999) && (dot < 1.0001)))
      {
        faces[i] = 1;
        triangleCenterX = (point1X[i]+point2X[i]+point3X[i])/3;
        triangleCenterY = (point1Y[i]+point2Y[i]+point3Y[i])/3;
        triangleCenterZ = (point1Z[i]+point2Z[i]+point3Z[i])/3;
        for (j = 0; j < maxMold; j++)       
        {
          triangleCenterZ2 = (point1Z[j]+point2Z[j]+point3Z[j])/3;
          if((triangleCenterZ > triangleCenterZ2)  && (i != j))
          {
            if(point_inside_trigon(triangleCenterX,triangleCenterY,point1X[j],point1Y[j],point2X[j],point2Y[j],point3X[j],point3Y[j]) == 1)
            {
              faces[i] = 0;
              flagBreak = 1;
            }
          }
          if(flagBreak == 1)
          {
            flagBreak = 0;
            break;
          }
        }
      }
    }

    return;
}

int point_inside_trigon(float sx, float sy, float ax, float ay, float bx, float by, float cx, float cy)
{
    float as_x = sx-ax;
    float as_y = sy-ay;

    int s_ab = 0;
    if((bx-ax)*as_y-(by-ay)*as_x > 0)
    {
      s_ab = 1;
    }

    if((cx-ax)*as_y-(cy-ay)*as_x > 0 == s_ab) return 0;

    if((cx-bx)*(sy-by)-(cy-by)*(sx-bx) > 0 != s_ab) return 0;

    return 1;
}

/*
bool intpoint_inside_trigon(intPoint s, intPoint a, intPoint b, intPoint c)
{
    int as_x = s.x-a.x;
    int as_y = s.y-a.y;

    bool s_ab = (b.x-a.x)*as_y-(b.y-a.y)*as_x > 0;

    if((c.x-a.x)*as_y-(c.y-a.y)*as_x > 0 == s_ab) return false;

    if((c.x-b.x)*(s.y-b.y)-(c.y-b.y)*(s.x-b.x) > 0 != s_ab) return false;

    return true;
}
*/