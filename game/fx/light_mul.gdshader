shader_type canvas_item;
render_mode blend_mul;
// Darkness with pools of restored light. Warm light is reserved for light the player has restored.
uniform float dark = 0.0;
uniform vec4 shade_color : source_color = vec4(0.26, 0.34, 0.42, 1.0);
uniform int n_lights = 0;
uniform vec4 lights[8];        // x, y, radius, hole (how strongly it clears the dark)
uniform vec2 area = vec2(1600.0, 1000.0);

void fragment() {
	vec2 p = UV * area;
	float clear = 0.0;
	for (int i = 0; i < 8; i++) {
		if (i >= n_lights) { break; }
		float d = length(p - lights[i].xy) / max(lights[i].z, 1.0);
		float k = 1.0 - smoothstep(0.0, 1.0, d);
		clear = max(clear, k * lights[i].w);
	}
	vec3 m = mix(vec3(1.0), shade_color.rgb, dark * (1.0 - clear));
	COLOR = vec4(m, 1.0);
}
