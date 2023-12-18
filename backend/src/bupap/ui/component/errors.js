export default {
  template: `<div></div>`,
  data() {
    return {
      errors: []
    };
  },
  methods: {
    show_short_error(short_msg, exc_type, exc_msg, traceback) {
      window.Quasar.Notify.create({
        message: short_msg,
        type: "negative",
        actions: [
          {
            label: 'Details', color: 'yellow', handler: () => {
              this.$emit('show_full_error', { short_msg: short_msg, exc_type: exc_type, exc_msg: exc_msg, traceback: traceback });
            }
          },
          { label: 'Dismiss', color: 'white'}
        ]
      });
    },
  }
};