shader_type canvas_item;
// the lake ripples for the first time: a slow horizontal shimmer on the lower part of the picture
uniform float amp = 0.0;
uniform float horizon = 0.58;
uniform float t = 0.0;
void fragment() {
	vec2 uv = UV;
	float below = smoothstep(horizon, horizon + 0.06, uv.y);
	uv.x += sin(uv.y * 90.0 + t * 2.4) * 0.006 * amp * below;
	uv.y += sin(uv.x * 50.0 + t * 1.7) * 0.003 * amp * below;
	COLOR = texture(TEXTURE, uv);
}
