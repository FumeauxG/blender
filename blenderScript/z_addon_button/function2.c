#include <stdio.h>
#include <math.h>

void select_faces(int *ptr, int max, float *normalX, float *normalY, float *normalZ, float maxAngle, float vecDirX, float vecDirY, float vecDirZ, int *faces, float *point1X, float *point1Y, float *point2X, float *point2Y, float *point3X, float *point3Y, float *point1Z, float *point2Z, float *point3Z);
int point_inside_trigon(float sx, float sy, float ax, float ay, float bx, float by, float cx, float cy);

void select_faces(int *ptr, int max, float *normalX, float *normalY, float *normalZ, float maxAngle, float vecDirX, float vecDirY, float vecDirZ, int *faces, float *point1X, float *point1Y, float *point2X, float *point2Y, float *point3X, float *point3Y, float *point1Z, float *point2Z, float *point3Z)
{
    int i;
    int j;

    float dot;
    float lenSq1;
    float lenSq2;
    float angle;
    float x2 = vecDirX;
    float y2 = vecDirY;
    float z2 = vecDirZ;
    
    //float triangleCenterX;
    //float triangleCenterY;
    //float triangleCenterZ;
    //float triangleCenterZ2;
    //float maxI;
    //float minJ;
    float dist1;
    float dist2;
    float dist3;

    for (i = 0; i < max; i++) 
    {
      //printf("%i\n", ptr[i]);

      dot = normalX[i]*x2 + normalY[i]*y2 + normalZ[i]*z2;    //between [x1, y1, z1] and [x2, y2, z2]
      lenSq1 = normalX[i]*normalX[i] + normalY[i]*normalY[i] + normalZ[i]*normalZ[i];
      lenSq2 = x2*x2 + y2*y2 + z2*z2;
      angle = acos(dot/sqrt(lenSq1 * lenSq2));

      if(angle < maxAngle || ((dot > 0.9999) && (dot < 1.0001)))
      {
        faces[i] = 1;
        //triangleCenterX = (point1X[i]+point2X[i]+point3X[i])/3;
        //triangleCenterY = (point1Y[i]+point2Y[i]+point3Y[i])/3;
        //triangleCenterZ = (point1Z[i]+point2Z[i]+point3Z[i])/3;
        /*
        if(point1Z[i] < point2Z[i])
        {
          if(point1Z[i] < point3Z[i])
          {
            triangleCenterZ = point1Z[i];
          }
          else
          {
            triangleCenterZ = point3Z[i];
          }
        }
        else
        {
          if(point2Z[i] < point3Z[i])
          {
            triangleCenterZ = point2Z[i];
          }
          else
          {
            triangleCenterZ = point3Z[i];
          }
        }
        
        if(point1Z[i] > point2Z[i])
        {
          if(point1Z[i] > point3Z[i])
          {
            maxI = point1Z[i];
          }
          else
          {
            maxI = point3Z[i];
          }
        }
        else
        {
          if(point2Z[i] > point3Z[i])
          {
            maxI = point2Z[i];
          }
          else
          {
            maxI = point3Z[i];
          }
        }
        */
        
        for (j = 0; j < max; j++)       
        {
          //triangleCenterZ2 = (point1Z[j]+point2Z[j]+point3Z[j])/3;
          /*
          if(point1Z[j] > point2Z[j])
          {
            if(point1Z[j] > point3Z[j])
            {
              triangleCenterZ2 = point1Z[j];
            }
            else
            {
              triangleCenterZ2 = point3Z[j];
            }
          }
          else
          {
            if(point2Z[j] > point3Z[j])
            {
              triangleCenterZ2 = point2Z[j];
            }
            else
            {
              triangleCenterZ2 = point3Z[j];
            }
          }
          
          if(point1Z[j] < point2Z[j])
          {
            if(point1Z[j] < point3Z[j])
            {
              minJ = point1Z[j];
            }
            else
            {
              minJ = point3Z[j];
            }
          }
          else
          {
            if(point2Z[j] < point3Z[j])
            {
              minJ = point2Z[j];
            }
            else
            {
              minJ = point3Z[j];
            }
          }
          */
          
          //if(((triangleCenterZ > triangleCenterZ2) || ((maxI<triangleCenterZ2)&&(minJ<triangleCenterZ))) && (i != j))
          //if((point1Z[i] > point2Z[j]) && (i != j))
          //if((triangleCenterZ > minJ) && (i != j))
          //if((triangleCenterZ > triangleCenterZ2) && (i != j))
          //float dist1 = (point1X[i]-point1X[j])*normalX[j] + (point1Y[i]-point1Y[j])*normalY[j] + (point1Z[i]-point1Z[j])*normalZ[j]; // your perpendicular distance
          //float dist2 = (point2X[i]-point1X[j])*normalX[j] + (point2Y[i]-point1Y[j])*normalY[j] + (point2Z[i]-point1Z[j])*normalZ[j]; // your perpendicular distance
          //float dist3 = (point3X[i]-point1X[j])*normalX[j] + (point3Y[i]-point1Y[j])*normalY[j] + (point3Z[i]-point1Z[j])*normalZ[j]; // your perpendicular distance

          dist1 = (point1X[i]-point1X[j])*normalX[j] + (point1Y[i]-point1Y[j])*normalY[j] + (point1Z[i]-point1Z[j])*normalZ[j]; // your perpendicular distance
          dist2 = (point2X[i]-point1X[j])*normalX[j] + (point2Y[i]-point1Y[j])*normalY[j] + (point2Z[i]-point1Z[j])*normalZ[j]; // your perpendicular distance
          dist3 = (point3X[i]-point1X[j])*normalX[j] + (point3Y[i]-point1Y[j])*normalY[j] + (point3Z[i]-point1Z[j])*normalZ[j]; // your perpendicular distance

          //float signN = normalX[j]*normalY[j]*normalZ[j];

          //if(((dist1 >= 0 && signN >= 0) || (dist1 <= 0 && signN <= 0)) && ((dist2 >= 0 && signN >= 0) || (dist2 <= 0 && signN <= 0)) && ((dist3 >= 0 && signN >= 0) || (dist3 <= 0 && signN <= 0)))
          //printf("dist1 %f\n", dist1);
          //printf("dist2 %f\n", dist2);
          //printf("dist3 %f\n", dist3);
          //printf("nz %f\n", normalZ[j]);
          //if(((dist1 > 0.001) && (dist2 > 0.001) && (dist3 > 0.001) && normalZ[j] > 0.001) || ((dist1 < -0.001) && (dist2 < -0.001) && (dist3 < -0.001) && normalZ[j] < -0.001))
          if(((dist1 > 0) && (dist2 > 0) && (dist3 > 0) && normalZ[j] > 0) || ((dist1 < 0) && (dist2 < 0) && (dist3 < 0) && normalZ[j] < 0))
          {
            if(point_inside_trigon(point1X[i],point1Y[i],point1X[j],point1Y[j],point2X[j],point2Y[j],point3X[j],point3Y[j]) == 1)
            {
              faces[i] = 0;
              break;
            }

            if(point_inside_trigon(point2X[i],point2Y[i],point1X[j],point1Y[j],point2X[j],point2Y[j],point3X[j],point3Y[j]) == 1)
            {
              faces[i] = 0;
              break;
            }

            if(point_inside_trigon(point3X[i],point3Y[i],point1X[j],point1Y[j],point2X[j],point2Y[j],point3X[j],point3Y[j]) == 1)
            {
              faces[i] = 0;
              break;
            }
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
    if((bx-ax)*as_y-(by-ay)*as_x >= 0)
    {
      s_ab = 1;
    }

    if(((cx-ax)*as_y-(cy-ay)*as_x >= 0) == s_ab) return 0;

    if(((cx-bx)*(sy-by)-(cy-by)*(sx-bx) >= 0) != s_ab) return 0;

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