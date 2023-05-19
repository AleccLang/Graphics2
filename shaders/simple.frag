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
    vec3 N = normalize(fragmentNormal); // normal to the surface
    vec3 L = normalize(lightPosition - fragmentPosition); // direction from fragment to the light source
    vec3 R = reflect(-L, N); // direction that perfectly reflected ray would take
    vec3 V = normalize(viewPosition - fragmentPosition); // direction from fragment to the viewer
    

    // Ambient light component
    vec3 ambientLight = ambientIntensity * lightColour;

    // Diffuse light component
    float kd = max(dot(N, L), 0.0);
    vec3 diffuseLight = kd * lightColour;

    // Specular light component 
    float ks = pow(max(dot(V, R), 0.0), shineCoefficient);
    vec3 specularLight = specularIntensity * ks * lightColour;

    return ambientLight + diffuseLight + specularLight;
}

void main() {
    vec3 firstLightComponents = calcLightComponents(firstLightPosition, firstLightColour, ambientIntensityFirst, specularIntensityFirst, shineCoefficientFirst); // The first light's 'light'
    vec3 secondLightComponents = calcLightComponents(secondLightPosition, secondLightColour, ambientIntensitySecond, specularIntensitySecond, shineCoefficientSecond); // The second light's 'light'

    vec4 texColour = texture(textureSampler, fragmentTextureCoord);
    vec3 result = (firstLightComponents + secondLightComponents) * vec3(texColour);

    OutColour = vec4(result, texColour.rgb);
}