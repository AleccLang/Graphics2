#version 330 core

layout (location=0) in vec3 vertexPosData;
layout (location=2) in vec3 vertexNormalData;
layout (location=1) in vec2 vertexTexCoordsData;

out vec3 fragmentPos;
out vec3 fragmentNormal;
out vec2 fragmentTexCoord;

uniform mat4 Model;
uniform mat4 View;
uniform mat4 Projection;

void main()
{
    gl_Position = Projection * View * Model * vec4(vertexPosData, 1.0);
    fragmentPos = vec3(Model * vec4(vertexPosData, 1.0));
    fragmentNormal = mat3(transpose(inverse(Model))) * vertexNormalData;
    fragmentTexCoord = vertexTexCoordsData;
}
