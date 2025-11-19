const PREF_KEY = 'lifeline_auth_persistence';

const getWindowStorage = (type) => {
  if (typeof window === 'undefined') {
    return null;
  }

  try {
    return type === 'local' ? window.localStorage : window.sessionStorage;
  } catch (err) {
    return null;
  }
};

const localStore = () => getWindowStorage('local');
const sessionStore = () => getWindowStorage('session');

const resolvePreference = () => {
  const local = localStore();
  const session = sessionStore();
  const localPref = local?.getItem(PREF_KEY);
  const sessionPref = session?.getItem(PREF_KEY);

  if (localPref === 'local') {
    return 'local';
  }

  if (sessionPref === 'session') {
    return 'session';
  }

  if (local?.getItem('access_token')) {
    return 'local';
  }

  if (session?.getItem('access_token')) {
    return 'session';
  }

  return 'session';
};

const storageFor = (persistence) => {
  if (persistence === 'local') {
    return localStore();
  }

  if (persistence === 'session') {
    return sessionStore();
  }

  return null;
};

export const getPreferredPersistence = () => resolvePreference();

export const setAuthPreference = (persistence) => {
  const local = localStore();
  const session = sessionStore();

  if (persistence === 'local') {
    local?.setItem(PREF_KEY, 'local');
    session?.removeItem(PREF_KEY);
  } else {
    session?.setItem(PREF_KEY, 'session');
    local?.removeItem(PREF_KEY);
  }
};

export const persistAuthItem = (key, value, persistence) => {
  const targetPersistence = persistence || resolvePreference();
  const storage = storageFor(targetPersistence) || sessionStore();
  const fallback = storage === localStore() ? sessionStore() : localStore();

  if (value === undefined || value === null) {
    storage?.removeItem(key);
    fallback?.removeItem(key);
    return;
  }

  storage?.setItem(key, value);
  fallback?.removeItem(key);
};

export const readAuthItem = (key) => {
  const primaryPersistence = resolvePreference();
  const primaryStore = storageFor(primaryPersistence) || sessionStore();
  const fallback = primaryStore === localStore() ? sessionStore() : localStore();

  const primaryValue = primaryStore?.getItem(key);
  if (primaryValue !== null && primaryValue !== undefined) {
    return primaryValue;
  }

  return fallback?.getItem(key) ?? null;
};

export const clearAuthStorage = () => {
  const local = localStore();
  const session = sessionStore();

  ['access_token', 'refresh_token', 'user', 'selectedCompanyId', 'current_user_id'].forEach((key) => {
    local?.removeItem(key);
    session?.removeItem(key);
  });

  local?.removeItem(PREF_KEY);
  session?.removeItem(PREF_KEY);
};
