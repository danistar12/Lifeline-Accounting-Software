// Small helper utilities to normalize API payloads by adding PascalCase aliases
// for snake_case fields (and simple name variants). This eases migration while
// the backend emits mixed naming styles.

function toPascalCase(key) {
  if (!key || typeof key !== 'string') return key;
  // split on underscores or spaces, also handle already camel/case by splitting on capital letters
  const parts = key.split(/[_\s]+/);
  return parts.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join('');
}

export function addPascalAliases(obj) {
  if (!obj || typeof obj !== 'object' || Array.isArray(obj)) return obj;

  const out = { ...obj };

  Object.keys(obj).forEach((k) => {
    const pascal = toPascalCase(k);
    // don't overwrite existing values
    if (!(pascal in out)) {
      out[pascal] = obj[k];
    }

    // If the value is an object (e.g., nested vendor/customer), recursively add aliases on that object
    if (obj[k] && typeof obj[k] === 'object' && !Array.isArray(obj[k])) {
      out[pascal] = addPascalAliases(out[pascal]);
    }
  });

  return out;
}

export function normalizeArray(arr) {
  if (!Array.isArray(arr)) return arr;
  return arr.map(item => addPascalAliases(item));
}

export default { addPascalAliases, normalizeArray };
