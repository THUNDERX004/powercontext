const baseUrl = process.env.STEPFUN_BASE_URL || "http://127.0.0.1:3000";

const response = await fetch(`${baseUrl}/api/health`);
const body = await response.json();
console.log(JSON.stringify(body, null, 2));
if (!response.ok || !body.ok) {
  process.exitCode = 1;
}
