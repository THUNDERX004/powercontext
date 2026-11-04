import http from "node:http";
import { createServer as createViteServer } from "vite";
import { config } from "./config.js";
import { createApplication } from "./app.js";
import { SeekdbStore } from "./seekdb-store.js";

async function main() {
  const store = new SeekdbStore();
  try {
    await store.initialize();
    console.log(
      `[stepfun] seekdb connected to ${config.seekdb.database} at ${config.seekdb.host}:${config.seekdb.port}`,
    );
  } catch (error) {
    console.error(
      `[stepfun] seekdb is not ready: ${error.message}. API health checks will retry.`,
    );
  }

  let vite;
  if (config.nodeEnv !== "production") {
    vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
  }

  const app = await createApplication({ store, vite });
  const server = http.createServer(app);

  server.listen(config.appPort, config.appHost, () => {
    console.log(
      `[stepfun] application listening at http://${config.appHost}:${config.appPort}`,
    );
  });

  async function shutdown(signal) {
    console.log(`[stepfun] received ${signal}; shutting down`);
    await new Promise((resolve) => server.close(resolve));
    await store.close().catch(() => {});
    if (vite) {
      await vite.close();
    }
  }

  process.on("SIGINT", () => shutdown("SIGINT").finally(() => process.exit(0)));
  process.on("SIGTERM", () => shutdown("SIGTERM").finally(() => process.exit(0)));
}

main().catch((error) => {
  console.error("[stepfun] failed to start", error);
  process.exitCode = 1;
});
