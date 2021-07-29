#include <stdio.h>
#include <math.h>

// Prototypes of functions
void select_faces(int *ptr, int max, float *normalX, float *normalY, float *normalZ, float maxAngle, float vecDirX, float vecDirY, float vecDirZ, int *faces, float *point1X, float *point1Y, float *point2X, float *point2Y, float *point3X, float *point3Y, float *point1Z, float *point2Z, float *point3Z);
int point_inside_trigon(float sx, float sy, float ax, float ay, float bx, float by, float cx, float cy);

void select_faces(int *ptr, int max, float *normalX, float *normalY, float *normalZ, float maxAngle, float vecDirX, float vecDirY, float vecDirZ, int *faces, float *point1X, float *point1Y, float *point2X, float *point2Y, float *point3X, float *point3Y, float *point1Z, float *point2Z, float *point3Z)
{
    // Variables of index
    int i;
    int j;

    float dot;    // Scalar product between v1 and v2
    float lenSq1; // Norme of v1 
    float lenSq2; // Norme of v2
    
    float angle;  // Angle between v1 and v2
    
    // Coefficents of v2
    float x2 = vecDirX;
    float y2 = vecDirY;
    float z2 = vecDirZ;
    
    float dist1;  // Distance between the first point and the plane
    float dist2;  // Distance between the second point and the plane
    float dist3;  // Distance between the third point and the plane

    // For each faces
    for (i = 0; i < max; i++) 
    {
      //printf("%i\n", ptr[i]);
      
      // Calculate the scalar product and the normes of v1 and v2
      dot = normalX[i]*x2 + normalY[i]*y2 + normalZ[i]*z2;    // Between [x1, y1, z1] and [x2, y2, z2]
      lenSq1 = normalX[i]*normalX[i] + normalY[i]*normalY[i] + normalZ[i]*normalZ[i];
      lenSq2 = x2*x2 + y2*y2 + z2*z2;
      // Calculate the angle between v1 and v2
      angle = acos(dot/sqrt(lenSq1 * lenSq2));

      // Check if the angle is inferior to the maxAngle
      if(angle < maxAngle || ((dot > 0.9999) && (dot < 1.0001)))
      {
        faces[i] = 1;   // Select the face
        
        // For each other face
        for (j = 0; j < max; j++)       
        {
          // Calculate the distance between the points of the faces from the plane of the other face
          dist1 = (point1X[i]-point1X[j])*normalX[j] + (point1Y[i]-point1Y[j])*normalY[j] + (point1Z[i]-point1Z[j])*normalZ[j]; // your perpendicular distance
          dist2 = (point2X[i]-point1X[j])*normalX[j] + (point2Y[i]-point1Y[j])*normalY[j] + (point2Z[i]-point1Z[j])*normalZ[j]; // your perpendicular distance
          dist3 = (point3X[i]-point1X[j])*normalX[j] + (point3Y[i]-point1Y[j])*normalY[j] + (point3Z[i]-point1Z[j])*normalZ[j]; // your perpendicular distance

          // If the face is higher than the other face
          if(((dist1 >= 0) && (dist2 >= 0) && (dist3 >= 0) && normalZ[j] > 0.001) || ((dist1 <= 0) && (dist2 <= 0) && (dist3 <= 0) && normalZ[j] < -0.001))
          {
            // Check if the points of the face are in the area of the other face
            if(point_inside_trigon(point1X[i],point1Y[i],point1X[j],point1Y[j],point2X[j],point2Y[j],point3X[j],point3Y[j]) == 1)
            {
              faces[i] = 0; // Deselect the face
              break;        // Leave the loop
            }

            if(point_inside_trigon(point2X[i],point2Y[i],point1X[j],point1Y[j],point2X[j],point2Y[j],point3X[j],point3Y[j]) == 1)
            {
              faces[i] = 0; // Deselect the face
              break;        // Leave the loop
            }

            if(point_inside_trigon(point3X[i],point3Y[i],point1X[j],point1Y[j],point2X[j],point2Y[j],point3X[j],point3Y[j]) == 1)
            {
              faces[i] = 0; // Deselect the face
              break;        // Leave the loop
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