// Adapted from the nicegui documentation: https://github.com/zauberzeug/nicegui/blob/main/examples/single_page_app/router_frame.js
export default {
    template: "<div><slot></slot></div>",
    mounted() {
      window.addEventListener("popstate", (event) => {
        if (event.state?.page) {
          // push_state: false prevents adding the opened page to the history
          this.$emit("open", { page: event.state.page, query_data: event.state.query_data, push_state: false }); 
          
        }
      });
      const connectInterval = setInterval(async () => {
        if (window.socket.id === undefined) return;
        this.$emit("open", {page: window.location.pathname, query_data: window.location.search, push_state: false });
        clearInterval(connectInterval);
      }, 10);
    },
    props: {},
  };