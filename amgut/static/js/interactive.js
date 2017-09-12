$(document).ready(function() {
  //Patching in Math.log2
  Math.log2 = Math.log2 || function(x) {
    return Math.log(x) / Math.LN2;
  };
  //Patching in findIndex for Internet Explorer
  // From https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/findIndex
  if (!Array.prototype.findIndex) {
    Array.prototype.findIndex = function(predicate) {
      if (this === null) {
        throw new TypeError('findIndex called on null or undefined');
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

/**
*
* Create a grouping object, with an array of all OTUs that group to a value
* in the given property
*
* @param {list} list of OTU objects, where each has taxonomic information
* about the OTU and compositional data
* @param {prop} property in the OTU object to group by.
*
* @return object with array of OTUs that match each parameter in the given property.
*
**/
function group(list, prop) {
  var grouped = {};
  for (var i = 0; i < list.length; i++) {
    var key = list[i][prop];
    grouped[key] = grouped[key] || [];
    grouped[key].push(list[i]);
  }
  return grouped;
};


/**
*
* Function to calculate the average of a list
*
* @param {list} list of numbers to average
*
* @return float average of the numbers
*
**/
function getAvg(list) {
  return list.reduce(function(x, y) {
    return x + y;
  }) / list.length;
};

/**
*
* Sums two arrays by position
*
* @param {a1} First array
* @param {ar2} second array
*
* @return summed array
*
* @error arrays are unequal length
*
**/
function sumArrays(ar1, ar2) {
  var sum = [];
  if (ar1.length == ar2.length) {
      for (var i = 0; i < ar1.length; i++) {
          sum.push(ar1[i] + ar2[i]);
      }
  }
  else {
    throw 'Arrays unequal length: ' + ar1.length + '  ' + ar2.length;
  }
  return sum;
};

/**
*
* Calculates the index of a matching OTU in a list of OTUs
*
* @param {list} list of OTU objects, where each has taxonomic information
* about the OTU and compositional data
* @param {otu} otu name to match
* @param {level} optional: The OTU level to match the given otu string at.
* Defaults to label, aka what is currently set to show in graphs.
*
* @return object with array of OTUs that match each parameter in the given property.
*
**/
function findOTU(list, otu, level) {
  var lvl = level || 'label';
  function inner(element, index, array) {
    if (element[lvl] == this) {
      return true;
    }
    return false;
  }
  return list.findIndex(inner, otu);
};

function filterSites(list, sites) {

};

/**
*
* Fills the available summary data dropdown
*
* @param {site} site to get information for, or blank to empty the dropdown
* @param {catDropdown} Jquery select object to fill with options
* @param {disable} optional: Whether to disable an empty dropdown. Default false
*
*
**/
function buildCats(site, catDropdown, disable) {
  disable = disable || false;
  catDropdown.html('');
  if (site === '' || site === undefined) {
    if (disable) {
      catDropdown.prop('disabled', true);
    }
  } else {
    site = site.toLowerCase();
    if (!available_summaries.hasOwnProperty(site)) {
      // Unknown site so can't build list of available metadata
      return;
    }
    catDropdown.append(new Option('', ''));
    for (var pos = 0; pos < available_summaries[site].length; pos++) {
      var cat = available_summaries[site][pos];
      catDropdown.append(new Option(translate_summaries[cat], cat));
    }
    catDropdown.prop('disabled', false);
  }
};

/**
*
* Collapses OTU information to a given taxonomic level and number of OTUs
*
* @param {dataset} list of OTU objects, where each has taxonomic information
* about the OTU and compositional data
* @param {level} phylogenetic level to collapse to
* @param {max} optional: Number of OTUs to collapse to. Default 10. The rest
* will be added to the `OTHER` category.
* @param {prev_level} Optional: Previous phylogenetic level.
* @param {focus} Optional: What OTU to focus on in prev_level. Used to filter
* collapse to only collapse using a specific OTU.
*
* @return list of objects, collapsed to the given taxonomic level. Each contains
* {label:'', data: [], phylum:'', level:''}
*
**/
function collapse(dataset, level, max, prev_level, focus, sites) {
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
  var phylum_order = ['Firmicutes', 'Bacteroidetes', 'Proteobacteria',
    'Actinobacteria', 'Verrucomicrobia', 'Tenericutes', 'Cyanobacteria',
    'Fusobacteria'];

  var max_otus = max || 8;
  var focus = focus || null;
  var filter_to = sites || null;
  var prev_level = prev_level || null;
  var groups = group(dataset, level);
  var collapsed = {};
  var summaries = [];
  for (var g in groups) {
    if (focus !== null && groups[g][0][prev_level] !== focus) {
      continue;
    }
    var otu = {label: g, data: groups[g][0].data, phylum: groups[g][0].phylum};
    if (g === '') { otu.label = 'Unspecified'; }
    // Collapse the OTUs found in the group into a single
    for (var i = 1; i < groups[g].length; i++) {
      otu.data = sumArrays(otu.data, groups[g][i].data);
    }

    collapsed[g] = otu;
    summaries.push([g, getAvg(otu.data)]);
  }

  //collapse further to max number of OTUs and color properly
  // Making sure to keep phyla order
  var phyla_dict = {};
  sorted = summaries.sort(function(a, b) { return b[1] - a[1]; });
  var loop = sorted.length;
  if (loop > max) {
    loop = max;
  }
  for (var i = 0; i < loop; i++) {
    // Add to existing phylum list or create new if not exist
    var otu = collapsed[sorted[i][0]];
    if (phyla_dict.hasOwnProperty(otu.phylum)) {
      phyla_dict[otu.phylum].push(otu);
    } else {
      phyla_dict[otu.phylum] = [otu];
    }
  }
  var further_collapsed = [];
  var nonstandard_phyla = [];
  // make sure things stay in order
  for (var i = 0; i < phylum_order.length; i++) {
    p = phylum_order[i];
    if (phyla_dict.hasOwnProperty(p)) {
      further_collapsed = further_collapsed.concat(phyla_dict[p]);
    }
  }
  // Recolor based on phyla counts, so each phyla is a different color, and
  //those within phyla a different shade of the same color
  phyla_colors = {};
  for (phyla in phyla_dict) {
    //Check if non-standard phyla and add if needed
    if (phylum_order.indexOf(phyla) === -1) {
      further_collapsed = further_collapsed.concat(phyla_dict[phyla]);
    }
    //Get colors for known phyla or black
    var color = phylum_colors[phyla] || ['#FFFFFF', '#000000'];
    if (phyla_dict[phyla].length == 1) {
      phyla_colors[phyla] = [chroma.bezier(color).scale().colors(3)[1]];
    } else {
      var num_colors = phyla_dict[phyla].length;
      phyla_colors[phyla] = chroma.scale(color).colors(num_colors);
    }
  }
  for (var i = 0; i < further_collapsed.length; i++) {
    var ph = further_collapsed[i].phylum;
    var color = chroma(phyla_colors[ph].pop()).css();
    further_collapsed[i].backgroundColor = color;
  }
  if (sorted.length > max) {
    // Create the OTHER category for the rest of the OTUs
    var other = {label: 'Other', data: collapsed[sorted[loop][0]].data,
                 backgroundColor: 'rgba(180,180,180)' };
    for (var i = loop + 1; i < sorted.length; i++) {
      other.data = sumArrays(other.data, collapsed[sorted[i][0]].data);
    }
    for (var i = 0; i < other.data.length; i++) {
      other.data[i] = Math.floor(other.data[i] * 10000) / 10000;
    }
    further_collapsed.push(other);
  }
  if (filter_to !== null) {
    further_collapsed = filterSites(further_collapsed, filter_to);
  }

  // Round data values to four decimals
  for (var pos = 0; pos < further_collapsed.length; pos++) {
    otu = further_collapsed[pos];
    otu.data = otu.data.map(function(c, i, a) {
      return +c.toFixed(4);
    });
  }
  return further_collapsed;
};

/**
*
* Calculates the log2 fold change between a given OTU list and the existing one
*
* @param {newData} list of OTU objects, where each has taxonomic information
* about the OTU and compositional data. Data array must be length 1.
* @param {rawData} list of OTU objects, where each has taxonomic information
* about the OTU and compositional data
* @param {level} The OTU level to collapse and match the given data at.
* @param {dataPos} In rawData, the position in the data array to compare to
* when calculating the fold change.
*
* @return array containg array of labels for the graph, and another array of the
* corresponding fold changes
*
**/
function calcFoldChange(newData, rawData, level, dataPos) {
  var foldChanges = [];
  var collapsed = collapse(rawData, level, 10000);
  var dataCollapsed = collapse(newData, level, 10000);
  for (var i = 0; i < dataCollapsed.length; i++) {
    var otu = dataCollapsed[i];
    var pos = findOTU(collapsed, otu.label);
    //sanity checks to make sure we aren't doing something dumb
    if (pos === -1 || otu.data === 0) {
      continue;
    }
    var sample_data = collapsed[pos].data;

    //Compute the fold changes, making them negative when needed
    var val = sample_data[dataPos] / otu.data;
    if (val === 0) {
      continue;
    }
    foldChanges.push([otu.label, Math.floor(Math.log2(val) * 100) / 100]);
  }
  //Sort by the average and build the data information
  var sorted = foldChanges.sort(function(a, b) {
    return b[1] - a[1];
  });
  foldData = [];
  labels = [];
  for (var i = 0; i < sorted.length; i++) {
    //TODO: Some way to filter significance
    foldData.push(sorted[i][1]);
    labels.push(sorted[i][0]);
  }
  return [labels, foldData];
};

/**
*
* Wraps calc_fold_change to get and show the fold change information on page
*
**/
function fold_change() {
  var level = $('#collapse-fold').val();
  var category = $('#meta-cat-fold').val();
  var barcode = $('#barcode-fold').val();
  //Set alpha diversity image going first, adds image.
  if (category === '') {
    $('#alpha-div-image').attr('src', '/interactive/alpha_div/' + barcode);
  } else {
      $('#alpha-div-image').attr('src', '/interactive/alpha_div/' + barcode +
        '?category=' + category);
  }
  $.get('/interactive/metadata/', {category: category, barcode: barcode})
    .done(function(data) {
      var dataPos = barChartFoldData.barcodes.findIndex(function(y) {
        return barcode == y;
      });
      var rawData = barChartSummaryData.rawData;
      foldChanges = calcFoldChange(data, rawData, level, dataPos);
      var labels = foldChanges[0];
      var foldData = foldChanges[1];
      barChartFoldData.labels = labels;
      barChartFoldData.datasets = [{
        backgroundColor: 'rgba(120,163,186,0.7)',
        strokeColor: 'rgba(151,187,205,0.8)',
        highlightBackground: 'rgba(220,220,220,1)',
        highlightStroke: 'rgba(220,220,220,1)',
        label: 'fold changes',
        data: foldData
      }];
      window.foldBar.update();
    })
    .fail(function() {
      alert('FAIL!');
    });
};

/**
*
* Helper function for adding metadata to existing interactive bar chart
*
* @param {target} list of OTU objects, where each has taxonomic information
* about the OTU and compositional data. Data array must be length 1.
* @param {newCol} list of OTU objects, where each has taxonomic information
* about the OTU and compositional data. Data array must be length 1.
* @param {collapseTo} The OTU level to collapse and match the given data at.
*
* @returns collapsed list of OTU objects with data from newCol integrated
*
**/
function addMetadata(target, newCol, collapseTo) {
  newLen = target[0].data.length + 1;
  for (var i = 0; i < newCol.length; i++) {
    var otu = newCol[i];
    var val = otu.data[0];
    var existing = findOTU(target, otu.full, 'full');
    if (existing == -1) {
      //add the OTU as zero for existing labels, then add value from meta-cat
      otu.data = new Array(newLen).join('0').split('').map(parseFloat);
      otu.data.push(val);
      target.push(otu);
    } else {
      // OTU already exists, so add to end of existing one
      target[existing].data.push(val);
    }
  }

  //Loop over raw data and add 0 to any OTUs in raw data but not in meta-cat
  var full_len = newLen;
  for (var i = 0; i < target.length; i++) {
    if (target[i].data.length < full_len) {
      target[i].data.push(0.0);
    }
  }

  return collapse(target, collapseTo, 10);
};

/**
*
* Gets new column data and displays it in the stacked bar chart.
*
**/
function add_metadata_barchart() {
  var category = $('#meta-cat').val();
  var site = $('#meta-site').val();
  var pos = barChartSummaryData.labels.length;
  //Don't do anything if they submit on empty value
  if (category.length === 0 || site.length === 0) {
    return;
  }
  var title = category + '  ' + site;
  //column already in graph, so don't add again
  if (barChartSummaryData.labels.indexOf(title) != -1) {
    return;
  }

  $.get('/interactive/metadata/', {category: category, site: site})
    .done(function(data) {
      barChartSummaryData.datasets = addMetadata(barChartSummaryData.metaData,
                                                 data, $('#collapse').val());
      barChartSummaryData.labels.push(title);
      window.summaryBar.update();
      var rem = $("<td><button href='#' onclick='remove_sample(\"" + title + "\"); return false;'>X</button></td>");
      $('#remove-row').append(rem);
    })
    .fail(function() {
      alert('FAIL!');
    });
};
/**
*
* Removes a column from the stacked bar chart
*
* @param {title} label of the column to remove.
*
**/
function remove_sample(title) {
  var data_pos = barChartSummaryData.labels.findIndex(function(y) {
    return title == y;
  });
  var to_remove = [];
  for (var i = 0; i < barChartSummaryData.metaData.length; i++) {
    barChartSummaryData.metaData[i].data.splice(data_pos, 1);
    // Check if every value in the remaining array is zero,
    // and if so set the OTU to be removed.
    var allZero = barChartSummaryData.metaData[i].data.every(function(y) {
      return y === 0.0;
    });
    if (allZero) {
      to_remove.push(i);
    }
  }
  //Remove OTU with all zero data(no longer relevant)
  for (var i = to_remove.length - 1; i >= 0; i--) {
    barChartSummaryData.metaData.splice(to_remove[i], 1);
  }

  barChartSummaryData.datasets = collapse(barChartSummaryData.metaData,
                                          $('#collapse').val(), 10);
  barChartSummaryData.labels.splice(data_pos, 1);
  window.summaryBar.update();
  $('td').eq(data_pos).remove();
  return false;
};
