#version 330 core

layout (location=0) in vec3 vertexPosition;
layout (location=1) in vec2 vertexTextureCoord;
layout (location=2) in vec3 vertexNormal;

uniform mat4 Model;
uniform mat4 View;
uniform mat4 Projection;

out vec2 fragmentTextureCoord;
out vec3 fragmentPosition;
out vec3 fragmentNormal;

void main()
{
    gl_Position = Projection * View * Model * vec4(vertexPosition, 1.0);
    fragmentTextureCoord = vertexTextureCoord;
    fragmentPosition = vec3(Model * vec4(vertexPosition, 1.0));
    fragmentNormal = mat3(transpose(inverse(Model))) * vertexNormal;
}
