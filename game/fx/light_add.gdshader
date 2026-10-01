shader_type canvas_item;
render_mode blend_add;
uniform int n_lights = 0;
uniform vec4 lights[8];        // x, y, radius, intensity
uniform vec4 colors[8];        // rgb, flicker
uniform vec2 area = vec2(1600.0, 1000.0);
uniform float t = 0.0;

float hash(float x) { return fract(sin(x * 127.1) * 43758.5453); }

void fragment() {
	vec2 p = UV * area;
	vec3 acc = vec3(0.0);
	for (int i = 0; i < 8; i++) {
		if (i >= n_lights) { break; }
		float d = length(p - lights[i].xy) / max(lights[i].z, 1.0);
		float k = 1.0 - smoothstep(0.0, 1.0, d);
		k = k * k;
		float fl = 1.0 + colors[i].a * (sin(t * 9.0 + float(i) * 3.1) * 0.5 + (hash(floor(t * 14.0) + float(i)) - 0.5));
		acc += colors[i].rgb * k * lights[i].w * fl * 0.42;
	}
	COLOR = vec4(acc, 1.0);
}
