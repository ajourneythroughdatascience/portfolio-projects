<?php
function topics_cloud_shortcode() {
    $taxonomy = 'topics'; // Your custom taxonomy name

    $terms = get_terms(array(
        'taxonomy' => $taxonomy,
        'hide_empty' => true,
    ));

    if (empty($terms)) {
        return '';
    }

    $output = '<div class="topics-cloud">';

    foreach ($terms as $term) {
        $term_link = get_term_link($term);
        if (is_wp_error($term_link)) {
            continue;
        }

        $output .= '<a href="' . esc_url($term_link) . '" class="topic">' . esc_html($term->name) . '</a> ';
    }

    $output .= '</div>';

    return $output;
}
add_shortcode('topics_cloud', 'topics_cloud_shortcode');