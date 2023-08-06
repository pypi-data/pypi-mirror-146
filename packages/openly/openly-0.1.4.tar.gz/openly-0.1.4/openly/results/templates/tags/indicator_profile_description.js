var tag = this;

tag.on('mount', function(){
    var indicator = tag.parent.indicator;
    tag.update({ description: indicator.baseline_comment });
});