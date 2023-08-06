(function() {

  function updateData(respText, elt) {
    let data = JSON.parse(respText)
    let self_echart_id = elt.getAttribute("_echarts_instance_")
    let chart = echarts.getInstanceById(self_echart_id)
    chart.setOption(data);
  };

  htmx.defineExtension("echad-table",{
    onEvent : function(name,evt){

      if (name == "htmx:beforeProcessNode"){
        let node_id = evt.target.id
        let data_id = "data-" + node_id
        let table = document.getElementById(node_id)
        let data_tag = document.getElementById(data_id)
        let data_json = JSON.parse(data_tag.innerText)
        let j = jspreadsheet(table,{
          data:data_json,
          fullscreen:true


        })

        

        

      }
    }


  })


  htmx.defineExtension('echad', {
    onEvent: function(name, evt) {

      if (name == "htmx:beforeProcessNode") {
        let node_id = evt.target.id
        let theme = evt.target.getAttribute("theme") || 'vintage'
        let data_id = "data-" + node_id
        let data = document.getElementById(data_id)
        if (!data) {
          echarts.init(document.getElementById(node_id), theme);

        } else {
          let data_option = JSON.parse(data.innerText)
          let c = echarts.init(document.getElementById(node_id), theme);
          echarts.getInstanceById(c.id).setOption(data_option)

        }

      }

      if (name == "htmx:afterSwap") {
        let elt = evt.target
        let self_echart_id = elt.getAttribute("_echarts_instance_")
        let chart = echarts.getInstanceById(self_echart_id)
        let text = evt.detail.xhr.responseText
        let data = JSON.parse(text)
        chart.setOption(data)

      }

    },

    transformResponse: function(text, xhr, elt) {
      let data = JSON.parse(text)
      let self_echart_id = elt.getAttribute("_echarts_instance_")
      let chart = echarts.getInstanceById(self_echart_id)
      chart.setOption(data);
      return text
    }

  })
})();