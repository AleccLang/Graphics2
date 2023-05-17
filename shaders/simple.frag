#version 330 core

uniform vec3 viewPosition;
uniform vec3 firstLightPosition;
uniform vec3 firstLightColour;
uniform vec3 secondLightPosition;
uniform vec3 secondLightColour;
uniform sampler2D textureSampler;

in vec2 fragmentTextureCoord;
in vec3 fragmentPosition;
in vec3 fragmentNormal;
out vec4 OutColour;

uniform float ambientIntensityFirst = 0.3;
uniform float ambientIntensitySecond = 0.3;
uniform float specularIntensityFirst = 0.9;
uniform float specularIntensitySecond = 0.9;
uniform float shineCoefficientFirst = 64;
uniform float shineCoefficientSecond = 64;

vec3 calcLightComponents(vec3 lightPosition, vec3 lightColour, float ambientIntensity, float specularIntensity, float shineCoefficient) {
    vec3 norm = normalize(fragmentNormal);
    vec3 lightDir = normalize(lightPosition - fragmentPosition); // direction from fragment to the light source
    vec3 viewDir = normalize(viewPosition - fragmentPosition); // direction from fragment to the viewer
    vec3 reflectDir = reflect(-lightDir, norm); // direction that perfectly reflected ray would take

    // Ambient light component
    vec3 amb = ambientIntensity * lightColour;

    // Diffuse light component
    float kd = max(dot(norm, lightDir), 0.0);
    vec3 diff = kd * lightColour;

    // Specular light component 
    float ks = pow(max(dot(viewDir, reflectDir), 0.0), shineCoefficient);
    vec3 spec = specularIntensity * ks * lightColour;

    return amb + diff + spec;
}

void main() {
    vec3 firstLightComponents = calcLightComponents(firstLightPosition, firstLightColour, ambientIntensityFirst, specularIntensityFirst, shineCoefficientFirst); // The first light's 'light'
    vec3 secondLightComponents = calcLightComponents(secondLightPosition, secondLightColour, ambientIntensitySecond, specularIntensitySecond, shineCoefficientSecond); // The second light's 'light'

    vec4 texColour = texture(textureSampler, fragmentTextureCoord);
    vec3 result = (firstLightComponents + secondLightComponents) * vec3(texColour);

    OutColour = vec4(result, texColour.rgb);
}