shader_type canvas_item;
render_mode blend_mix;
// light film grain
uniform float amount = 0.022;
uniform float t = 0.0;
float hash(vec2 p) {
	p = fract(p * vec2(123.34, 456.21));
	p += dot(p, p + 45.32);
	return fract(p.x * p.y);
}
void fragment() {
	float n = hash(floor(UV * vec2(1600.0, 1000.0) * 0.5) + floor(t * 12.0) * 17.0);
	float a = abs(n - 0.5) * 2.0 * amount;
	COLOR = vec4(vec3(step(0.5, n)), a);
}
