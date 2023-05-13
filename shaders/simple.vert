#version 330 core

layout (location=0) in vec3 position;
layout (location=1) in vec2 textureCoord;
layout (location=2) in vec3 normal;

uniform mat4 Model;
uniform mat4 View;
uniform mat4 Projection;

out vec2 fragmentTextureCoord;
out vec3 fragmentPosition;
out vec3 fragmentNormal;

void main()
{
    gl_Position = Projection * View * Model * vec4(position, 1.0);
    fragmentTextureCoord = textureCoord;
    fragmentPosition = vec3(Model * vec4(position, 1.0));
    fragmentNormal = mat3(transpose(inverse(Model))) * normal;
}
