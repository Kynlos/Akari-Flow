# API Documentation

*Last updated: 1763154087.6357105*

### API Documentation for Database Module
#### Overview of Changes
The `database.ts` file has been updated with new exports and modifications to existing functions. This documentation outlines the changes, new functions, and usage examples.

#### New/Modified Functions and Classes
The following exports have been added or modified:
* `class Database`: A class representing a database connection.
* `export async function createConnection(config: DatabaseConfig)`: Creates a new database connection based on the provided configuration.
* `export function sanitizeInput(input: string)`: Sanitizes user input to prevent SQL injection attacks.
* `interface DatabaseConfig`: Defines the configuration options for a database connection.

#### Usage Examples
##### Creating a Database Connection
```typescript
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = {
  // configuration options
  host: 'localhost',
  port: 5432,
  username: 'user',
  password: 'password',
  database: 'mydb',
};

createConnection(config).then((connection) => {
  // use the connection
}).catch((error) => {
  // handle error
});
```

##### Sanitizing User Input
```typescript
import { sanitizeInput } from './database';

const userInput = "Robert'); DROP TABLE Students; --";
const sanitizedInput = sanitizeInput(userInput);
console.log(sanitizedInput); // sanitized input
```

#### Migration Notes
The `createConnection` function now returns a promise that resolves to a `Database` object. If you were previously using the `createConnection` function with a callback, you will need to update your code to use the promise-based approach.

```typescript
// before
createConnection(config, (error, connection) => {
  // use the connection
});

// after
createConnection(config).then((connection) => {
  // use the connection
}).catch((error) => {
  // handle error
});
```

Note that the `DatabaseConfig` interface has been added to define the configuration options for a database connection. You should update your code to use this interface when creating a new database connection.

```typescript
// before
const config = {
  host: 'localhost',
  port: 5432,
  username: 'user',
  password: 'password',
  database: 'mydb',
};

// after
const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  username: 'user',
  password: 'password',
  database: 'mydb',
};
```