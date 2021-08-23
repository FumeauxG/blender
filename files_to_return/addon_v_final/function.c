#include <stdio.h>
#include <math.h>

// Prototypes of functions
void select_faces(int *ptr, int max, float *normalX, float *normalY, float *normalZ, float maxAngle, float vecDirX, float vecDirY, float vecDirZ, int *faces, 
                  float *point1X, float *point1Y, float *point2X, float *point2Y, float *point3X, float *point3Y, float *point1Z, float *point2Z, float *point3Z);
int point_inside_trigon(float sx, float sy, float ax, float ay, float bx, float by, float cx, float cy);

/*---------------------------------------------------------
  But : 
    This method selects all the faces where the angle 
    between the face and the downward vector is less than 
    the maxAngle and then the selected faces don't have
    other faces under.
  ---------------------------------------------------------
  Parameters :
    ptr : index of the faces
    max : number of the faces
    normalX : x component of the normal
    normalY : y component of the normal    
    normalZ : z component of the normal
    maxAngle : value of the angle maximum in radians
    vecDirX : x component of the downward vector
    vecDirY : y component of the downward vector
    vecDirZ : z component of the downward vector
    faces : result of the selected faces
    point1X : x component of the first point of the faces
    point1Y : y component of the first point of the faces
    point1Z : z component of the first point of the faces
    point2X : x component of the second point of the faces
    point2Y : y component of the second point of the faces
    point2Z : z component of the second point of the faces
    point3X : x component of the third point of the faces
    point3Y : y component of the third point of the faces
    point3Z : z component of the third point of the faces
  Return : 
    void (the information to know if a face is selected
          is in the parameter faces)
---------------------------------------------------------*/
void select_faces(int *ptr, int max, float *normalX, float *normalY, float *normalZ, float maxAngle, float vecDirX, float vecDirY, float vecDirZ, int *faces, 
                  float *point1X, float *point1Y, float *point2X, float *point2Y, float *point3X, float *point3Y, float *point1Z, float *point2Z, float *point3Z)
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


/*---------------------------------------------------------
  But : 
    This method determine if a point is in the area of
    a triangle in 2D.
  ---------------------------------------------------------
  Parameters :
    sx : x component of point
    sy : x component of point
    ax : x component of the first vertix of the triangle
    ay : y component of the first vertix of the triangle
    bx : x component of the second vertix of the triangle
    by : y component of the second vertix of the triangle
    cx : x component of the third vertix of the triangle
    cy : y component of the third vertix of the triangle
  Return : 
    int : 1 if the point is inside the triangée
          0 if the point is not inside the triangée
---------------------------------------------------------*/
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