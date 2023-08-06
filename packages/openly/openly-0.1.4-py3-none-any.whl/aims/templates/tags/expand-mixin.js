/* Adds functionality for a tag to expand/collapse its displayed elements through the
 * toggle_expand method which should be passed as an onclick event handler to an appropriate
 * button in the tag.
 *
 * @param tag - The tag the mixin is being added to
 * @param displayed_array - The key for the tag's array of the elements to be displayed
 * @param total_array - The key for the tag's array of the all the elements
 * @param collapsed_num_shown - The number of elements to show when collapsed
 */
function ExpandMixin(tag, displayed_array, total_array, collapsed_num_shown) {
    this.init = function() {
	tag.expanded = false;
    }

    tag.on('mount', function() {
	tag.update_display();
    });

    tag.update_display = function() {
	if (tag.expanded) {
	    tag[displayed_array] = tag[total_array];
	} else {
	    tag[displayed_array] = tag[total_array].slice(0, collapsed_num_shown);
	}
	tag.update();
    }

    tag.toggle_expand = function() {
	tag.expanded = !tag.expanded;
	tag.update_display();
    }
}
