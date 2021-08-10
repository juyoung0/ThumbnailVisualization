
Vue.component('show-result', {
    props: ['values'],
    template: `
        <ul>
          <li v-for="(value, index) in values">
             Thumbnail {{ index }} :  Mean  {{ value.mean }},  Std : {{ value.std }}
          </li>
        </ul>
    `
})

Vue.component('show-table', {
    props: ['values', 'columns'],
    template: `
      <table class="table">
        <thead>
          <tr>
            <th scope="col" v-for="key in columns">
              {{ key }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in values">
            <th scope="row"> {{ entry.text }} </th>
            <td v-for="element in entry.child">
              {{ element.val }}
            </td>
          </tr>
        </tbody>
      </table>
    `
})

Vue.component('show-table2', {
    props: ['values', 'columns'],
    template: `
      <table class="table">
        <thead>
          <tr>
            <th scope="col" v-for="key in columns">
              {{ key }}
            </th>
          </tr>
        </thead>
        <tbody>
          <td v-for="entry in values">
              {{ entry.val }}
          </td>
        </tbody>
      </table>
    `
})

Vue.component('show-table3', {
    props: ['values', 'columns'],
    template: `
      <table class="table">
        <thead>
          <tr>
            <th scope="col" v-for="key in columns">
              {{ key }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in values">
            <td v-for="key in columns">
              {{ entry[key] }}
            </td>
          </tr>
        </tbody>
      </table>
    `
})

Vue.component('show-table4', {
    props: ['values', 'columns','questions'],
    template: `
      <table class="table">
        <thead>
          <tr>
            <th scope="col" v-for="key in questions">
              {{ key.question }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in values">
            <td v-for="key in columns">
              {{ entry[key] }}
            </td>
          </tr>
        </tbody>
      </table>
    `
})

Vue.component('show-image', {
    props: ['src'],
    template: `
        <div>
          <b-img src="src" fluid />
        </div>
    `
})

Vue.component('line-chart', {
  extends: VueChartJs.Line,
  mounted () {
    this.renderChart({
      labels: this.label,      datasets: [
        {
          label: 'Data One',
          backgroundColor: '#f87979',
          data: this.data
                  }
      ]
    }, {responsive: true, maintainAspectRatio: false})
  }
})

Vue.component('bar-chart', {
  extends: VueChartJs.Bar,
  props: ['columns','label', 'data'],
  mounted () {
    this.renderChart({
      labels: this.columns,
      datasets: [
        {
          label: this.label,
          backgroundColor: '#f87979',
          data: this.data,
        }
      ],
    }, {responsive: true, maintainAspectRatio: false,
            scales: {
               yAxes: [{
                  ticks: {
                   min: 0,
                  }
               }]
            }
    })
  }
})

Vue.component('bar-chart2', {
  extends: VueChartJs.Bar,
  props: ['columns','label', 'data', 'ticks'],
  mounted () {
    this.renderChart({
      labels: this.columns,
      datasets: [
        {
          label: this.label,
          backgroundColor: '#f87979',
          data: this.data,
        }
      ],
    }, {responsive: true, maintainAspectRatio: false,
        scales: {
               yAxes: [{
                  ticks: {
                   min: this.ticks.min,
                   max: this.ticks.max,
                  }
               }]
            }
    })
  }
})