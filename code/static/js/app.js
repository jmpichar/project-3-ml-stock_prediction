function buildPlayerdata(player) {
    d3.json(`/player/${player}` ).then((data) => {
        // Use d3 to select the panel with id of `#sample-metadata`
        var PANEL = d3.select("#sample-metadata");

        // Use `.html("") to clear any existing metadata
        PANEL.html("");


        Object.entries(data).forEach(([key, value]) => {
          PANEL.append("h6").text(`${key}: ${value}`);
        });

    })
}

function buildCharts() {
    d3.json('/players').then((data) => {
        console.log(data)
        var player1_name = data['players'][0]['name']
        var player2_name = data['players'][1]['name']
        var player1_chips = data['players'][0]['chips']
        var player2_chips = data['players'][1]['chips']

        console.log(player1_name)
        console.log(player2_name)
        var data = [
        {
            x: [player1_name, player2_name],
            y: [player1_chips,player2_chips ],
            type: 'bar'
        }
    ];

    Plotly.newPlot('bar', data);

  });
}

function init() {
    var selector = d3.select("#selDataset");
    // Use the list of sample names to populate the select options
    d3.json("/players").then((playerNames) => {
    playerNames['players'].forEach((p) => {
        player = p.name;
        selector
        .append("option")
        .text(player)
        .property("value", player);
    });

    // Use the first sample from the list to build the initial plots
    const firstPlayer = playerNames['players'][0]['name'];
    buildCharts()
    buildPlayerdata(firstPlayer);

    });
};

function optionChanged(newPlayer) {
  // Fetch new data each time a new player is selected
  buildCharts();
  buildPlayerdata(newPlayer);
}

init();
