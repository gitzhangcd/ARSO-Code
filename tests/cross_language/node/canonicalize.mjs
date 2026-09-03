import canonicalize from "canonicalize";

let input = "";
for await (const chunk of process.stdin) {
  input += chunk;
}

const value = JSON.parse(input);
const output = canonicalize(value);
if (output === undefined) {
  throw new Error("canonicalize returned undefined");
}
process.stdout.write(output);
