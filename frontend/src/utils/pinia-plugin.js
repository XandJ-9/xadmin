export const piniaPluginPersistedState = ({ store }) => {
    const key = `pinia-${store.$id}`;
    const persistedData = JSON.parse(localStorage.getItem(key));
 
    if (persistedData) {
        store.$patch(persistedData);
    }
 
    store.$subscribe((mutation, state) => {
        localStorage.setItem(key, JSON.stringify(state));
    });
};
