var phylum_colors = {
  'Firmicutes': ['pink', 'darkred'],
  'Bacteroidetes': ['#FFD27F', '#BE5E00'],
  'Proteobacteria': ['lightyellow', 'yellow'],
  'Actinobacteria': ['#F3DBAB', '#735B2B'],
  'Verrucomicrobia': ['#C5D991', '#465A12'],
  'Tenericutes': ['lightgreen', 'darkgreen'],
  'Cyanobacteria': ['lightcyan', 'darkcyan'],
  'Fusobacteria': ['lightblue', 'darkblue']
};
var phylum_order = ['Firmicutes', 'Bacteroidetes', 'Proteobacteria', 'Actinobacteria', 'Verrucomicrobia', 'Tenericutes', 'Cyanobacteria', 'Fusobacteria'];

$(document).ready(function() {
  //Patching for Internet Explorer
  if (!Array.prototype.findIndex) {
    Array.prototype.findIndex = function(predicate) {
      if (this === null) {
        throw new TypeError('Array.prototype.findIndex called on null or undefined');
      }
      if (typeof predicate !== 'function') {
        throw new TypeError('predicate must be a function');
      }
      var list = Object(this);
      var length = list.length >>> 0;
      var thisArg = arguments[1];
      var value;

      for (var i = 0; i < length; i++) {
        value = list[i];
        if (predicate.call(thisArg, value, i, list)) {
          return i;
        }
      }
      return -1;
    };
  }
});

function group(list, prop) {
  var grouped = {};
  for(var i=0;i<list.length;i++) {
    var key = list[i][prop];
    grouped[key] = grouped[key] || [];
    grouped[key].push(list[i]);
  }
  return grouped;
}

function getAvg(list) {
  return list.reduce(function (x, y) {
    return x + y;
  }) / list.length;
}

function sum_arrays(ar1, ar2) {
  var sum = [];
  if (ar1.length == ar2.length) {
      for (var i=0; i<ar1.length;i++) {
          sum.push(ar1[i] + ar2[i]);
      }
  }
  else {
    throw "Arrays unequal length: " + ar1.length + "  " + ar2.length;
  }
  return sum;
}

function find_otu(list, otu, level) {
  var lvl = level || 'label';
  function inner(element, index, array) {
    if(element[lvl] == this) { return true; }
    return false;
  }
  return list.findIndex(inner, otu);
}

function filter_sites(list, sites) {

}

function collapse(dataset, level, max, prev_level, focus, sites) {
  var max_otus = max || 8;
  var focus_taxa = focus || null;
  var filter_to = sites || null;
  var groups = group(dataset, level);
  var collapsed = {};
  var summaries = [];
  for(var g in groups) {
    if(focus !== null && groups[g][0][prev_level] != focus_taxa) { continue; }
    var otu = { label: g,  data: groups[g][0].data, phylum: groups[g][0].phylum};
    if(g === "") { otu.label = 'Unspecified'; }
    // Collapse the OTUs found in the group into a single
    for(var i=1;i<groups[g].length;i++) {
      otu.data = sum_arrays(otu.data, groups[g][i].data);
    }
    // Round to four decimals
    for(var i=0;i<otu.data.length;i++) { otu.data[i] = Math.floor(otu.data[i] * 10000) / 10000; }

    collapsed[g] = otu;
    summaries.push([g, getAvg(otu.data)]);
  }

  //collapse further to max number of OTUs and color properly
  // Making sure to keep phyla order
  var phyla_dict = {};
  sorted = summaries.sort(function(a, b) { return b[1] - a[1]; });
  var loop = sorted.length;
  if(loop > max) { loop = max; }
  for(var i=0;i<loop;i++) {
    // Add to existing phylum list or create new if not exist
    if(phyla_dict.hasOwnProperty(collapsed[sorted[i][0]].phylum)) {
      phyla_dict[collapsed[sorted[i][0]].phylum].push(collapsed[sorted[i][0]]);
    } else {
      phyla_dict[collapsed[sorted[i][0]].phylum] = [collapsed[sorted[i][0]]];
    }
  }
  var further_collapsed = [];
  var nonstandard_phyla = [];
  // make sure things stay in order
  for(var i=0;i<phylum_order.length;i++) {
    p = phylum_order[i];
    if(phyla_dict.hasOwnProperty(p)) {
      further_collapsed = further_collapsed.concat(phyla_dict[p]);
    }
  }
  // Recolor based on phyla counts, so each phyla is a different color, and those within phyla a different shade
  // of the same color
  phyla_colors = {};
  for(phyla in phyla_dict) {
    //Check if non-standard phyla and add if needed
    if(phylum_order.indexOf(phyla) === -1) { further_collapsed = further_collapsed.concat(phyla_dict[phyla]); }
    //Get colors for known phyla or black
    var color = phylum_colors[phyla]  || ['#FFFFFF', '#000000'];
    if(phyla_dict[phyla].length == 1) {
      phyla_colors[phyla] = [chroma.bezier(color).scale().colors(3)[1]];
    } else {
      phyla_colors[phyla] = chroma.scale(color).colors(phyla_dict[phyla].length);
    }
  }
  for(var i=0;i<further_collapsed.length;i++) {
    var ph = further_collapsed[i].phylum;
    var color = chroma(phyla_colors[ph].pop()).css();
    further_collapsed[i].backgroundColor = color;
  }
  if(sorted.length > max) {
    // Create the OTHER category for the rest of the OTUs
    var other = { label: 'Other',  data:collapsed[sorted[loop][0]].data, backgroundColor: 'rgba(180,180,180)' };
    for(var i=loop+1;i<sorted.length;i++){
      other.data = sum_arrays(other.data, collapsed[sorted[i][0]].data);
    }
    for(var i=0;i<other.data.length;i++) { other.data[i] = Math.floor(other.data[i] * 10000) / 10000; }
    further_collapsed.push(other);
  }
  if(filter_to !== null) {
    further_collapsed = filter_sites(further_collapsed, filter_to);
  }

  return further_collapsed;
}

function fold_change() {
  var level = $("#collapse-fold").val();
  var category = $("#meta-cat-fold").val();
  var barcode = $("#barcode-fold").val();
  //Don't do anything if they submit on empty barcode value
  if(barcode === "") {
    barChartFoldData.labels = [];
    barChartFoldData.datasets = [];
    window.foldBar.update();
    $("#alpha-div-image").attr("src", "");
    return;
  }
  //If there's no category, just update alpha diversity graph to show new barcode
  //Set alpha diversity image going first
  if(category === "") {
    $("#alpha-div-image").attr("src", "/interactive/alpha_div/" + barcode);
  } else {
      $("#alpha-div-image").attr("src", "/interactive/alpha_div/" + barcode + "?category=" + category);
  }

  $.get('/interactive/metadata/', {category: category, barcode: barcode})
    .done(function (data) {
      //Set alpha diversity image going first
      $("#alpha-div-image").attr("src", "/interactive/alpha_div/" + barcode + "?category=" + category);

      var fold_changes = [];
      var data_pos = barChartFoldData.barcodes.findIndex(function(y) { return barcode == y; });
      var collapsed = collapse(barChartSummaryData.rawData, level, 10000);
      var data_collapsed = collapse(data, level, 10000);
      for(var i=0;i<data_collapsed.length;i++) {
        var otu = data_collapsed[i];
        var pos = find_otu(collapsed, otu.label);
        //sanity checks to make sure we aren't doing something dumb
        if(pos === -1 || otu.data === 0) { continue; }
        var sample_data = collapsed[pos].data;

        //Compute the fold changes, making them negative when needed
        var val = sample_data[data_pos]/otu.data;
        if(val === 0) { continue; }
        fold_changes.push([otu.label, Math.floor(Math.log2(val) * 100) / 100]);
      }
      //Sort by the average and build the data information
      var sorted = fold_changes.sort(function(a, b) { return b[1] - a[1]; });
      fold_data = [];
      labels = [];
      for(var i=0;i<sorted.length;i++) {
        //TODO: Some way to filter significance
        fold_data.push(sorted[i][1]);
        labels.push(sorted[i][0]);
      }
      barChartFoldData.labels = labels;
      barChartFoldData.datasets = [{
        backgroundColor: "rgba(151,187,205,0.7)",
        strokeColor: "rgba(151,187,205,0.8)",
        highlightBackground: "rgba(220,220,220,1)",
        highlightStroke: "rgba(220,220,220,1)",
        label: "fold changes",
        data: fold_data
      }];
      window.foldBar.update();
    })
    .fail(function () {
      alert('FAIL!');
    });
}

function add_metadata_barchart() {
  var category = $("#meta-cat").val();
  var site = $("#meta-site").val();
  var pos = barChartSummaryData.labels.length;
  //Don't do anything if they submit on empty value
  if(category.length == 0 || site.length == 0) { return; }
  var title = category + "  " + site;
  //column already in graph, so don't add again
  if(barChartSummaryData.labels.indexOf(title) != -1) { return; }

  $.get('/interactive/metadata/', {category: $("#meta-cat").val(), site: $("#meta-site").val()})
    .done(function (data) {
      for(var i=0;i<data.length;i++) {
        var otu = data[i];
        var val = otu.data[0];
        var existing = find_otu(barChartSummaryData.metaData, otu.full, 'full');
        if(existing == -1) {
          //add the OTU as zero for all existing labels, then add value from meta-cat
          otu.data = new Array(barChartSummaryData.labels.length+1).join('0').split('').map(parseFloat);
          otu.data.push(val);
          barChartSummaryData.metaData.push(otu);
        } else {
          ///OTU already exists, so add to end of existing one
          barChartSummaryData.metaData[existing].data.push(val);
        }
      }

      //Loop over raw data and add 0 to any OTUs that are in raw data but not in meta-cat
      var full_len = barChartSummaryData.labels.length + 1;
      for(var i=0;i<barChartSummaryData.metaData.length;i++) {
        if(barChartSummaryData.metaData[i].data.length < full_len) { barChartSummaryData.metaData[i].data.push(0.0); }
      }

      barChartSummaryData.labels.push(title);
      barChartSummaryData.datasets = collapse(barChartSummaryData.metaData, $("#collapse").val(), 10);
      window.summaryBar.update();
      var rem = $('<td><a href="#" onclick="remove_sample(\'' + title + '\'); return false;">Remove</a></td>');
      $("#remove-row").append(rem);
    })
    .fail(function () {
      alert ('FAIL!');
    });
}

function remove_sample(title) {
  var data_pos = barChartSummaryData.labels.findIndex(function(y) { return title == y; });
  var to_remove = [];
  for(var i=0;i<barChartSummaryData.metaData.length;i++) {
    barChartSummaryData.metaData[i].data.splice(data_pos, 1);
    if(barChartSummaryData.metaData[i].data.every(function (y) { return y === 0.0; })) { to_remove.push(i); }
  }

  //Remove OTU with all zero data(no longer relevant)
  for(var i=to_remove.length-1;i>=0;i--) { barChartSummaryData.metaData.splice(to_remove[i], 1); }

  barChartSummaryData.datasets = collapse(barChartSummaryData.metaData, $("#collapse").val(), 10);
  barChartSummaryData.labels.splice(data_pos, 1);
  window.summaryBar.update();
  $("td").eq(data_pos).remove();
}