shader_type canvas_item;
// soft vignette (multiply-ish via alpha black)
uniform float strength = 0.55;
void fragment() {
	vec2 q = UV - 0.5;
	q.x *= 1.15;
	float d = length(q) * 1.45;
	float v = smoothstep(0.35, 1.05, d);
	COLOR = vec4(0.0, 0.0, 0.0, v * strength);
}
