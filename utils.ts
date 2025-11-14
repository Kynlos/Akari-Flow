/**
 * Utility functions for the application
 */

export interface StringOptions {
  trim?: boolean;
  lowercase?: boolean;
}

/**
 * Formats a string according to the provided options.
 *
 * @param input - The string to format.
 * @param options - Optional formatting options.
 * @returns The formatted string.
 */
export function formatString(input: string, options?: StringOptions): string {
  let result = input;
  
  if (options?.trim) {
    result = result.trim();
  }
  
  if (options?.lowercase) {
    result = result.toLowerCase();
  }
  
  // Small update to trigger bot
  return result;
}

/**
 * Parses a JSON string into an object.
 *
 * @param jsonString - The JSON string to parse.
 * @returns The parsed object, or `null` if parsing fails.
 */
export function parseJSON<T>(jsonString: string): T | null {
  try {
    return JSON.parse(jsonString);
  } catch {
    return null;
  }
}

export class Logger {
  private prefix: string;
  
  constructor(prefix: string = '[LOG]') {
    this.prefix = prefix;
  }
  
  log(message: string): void {
    console.log(`${this.prefix} ${message}`);
  }
  
  error(message: string): void {
    console.error(`${this.prefix} [ERROR] ${message}`);
  }
}
