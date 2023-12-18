<template>
  <div></div>
</template>

<script>
export default {
  async mounted() {
    await this.$nextTick();
    Plotly.newPlot(this.$el.id, this.options.data, this.options.layout, this.options.config);
    var self=this
    this.$el.on('plotly_click', function(data){
        console.log(data);
        self.$emit("data_click", {event: data.event, points:data.points.map((p) => 
        (({ data, fullData, xaxis, yaxis, ...object }) => object)(p)
     
        )})
    });
  },

  methods: {
    update(options) {
      Plotly.update(this.$el.id, options.data, options.layout, options.config);
    },
    
  },

  props: {
    options: Object,
  },
};
</script>

<style>
/*
  fix styles to correctly render modebar, otherwise large
  buttons with unwanted line breaks are shown, possibly
  due to other CSS libraries overriding default styles
  affecting plotly styling.
*/
.js-plotly-plot .plotly .modebar-group {
  display: flex;
}
.js-plotly-plot .plotly .modebar-btn {
  display: flex;
}
.js-plotly-plot .plotly .modebar-btn svg {
  position: static;
}
</style>
