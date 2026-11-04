import mysql from "mysql2/promise";
import { config } from "../server/config.js";

const connection = await mysql.createConnection({
  host: config.seekdb.host,
  port: config.seekdb.port,
  user: config.seekdb.user,
  password: config.seekdb.password,
  charset: config.seekdb.charset,
});

try {
  await connection.query(
    `CREATE DATABASE IF NOT EXISTS ${mysql.escapeId(config.seekdb.database)}
     CHARACTER SET utf8mb4`,
  );
  console.log(`Database ready: ${config.seekdb.database}`);
} finally {
  await connection.end();
}
