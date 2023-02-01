<?php


if (! defined('WP_DEBUG')) {
	die( 'Direct access forbidden.' );
}

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'child-style', get_template_directory_uri() . '/style.css' );
});
// 
// BEGIN ENQUEUE PARENT ACTION
// AUTO GENERATED - Do not modify or remove comment markers above or below:

if ( !function_exists( 'chld_thm_cfg_locale_css' ) ):
    function chld_thm_cfg_locale_css( $uri ){
        if ( empty( $uri ) && is_rtl() && file_exists( get_template_directory() . '/rtl.css' ) )
            $uri = get_template_directory_uri() . '/rtl.css';
        return $uri;
    }
endif;
add_filter( 'locale_stylesheet_uri', 'chld_thm_cfg_locale_css' );
         
if ( !function_exists( 'child_theme_configurator_css' ) ):
    function child_theme_configurator_css() {
        wp_enqueue_style( 'chld_thm_cfg_child', trailingslashit( get_stylesheet_directory_uri() ) . 'style.css', array( 'astra-theme-css','child-style' ) );
    }
endif;
add_action( 'wp_enqueue_scripts', 'child_theme_configurator_css', 10 );

// END ENQUEUE PARENT ACTION

// START PABLO CUSTOM FUNCTIONS

// ALLOW MULTIPLE CUSTOM POST TYPES IN ELEMENTOR POST WIDGET
add_action( 'elementor/query/multiple_cpts', function( $query ) {
	$query->set( 'post_type', [ 'blog', 'deep-dives', 'guided-projects', 'portfolio', 'documentation' ] );
} );

// ADD FEATURED IMAGE COLUMN TO ADMIN VIEW
// Set thumbnail size
add_image_size( 'pablo_admin-featured-image', 60, 60, false );

// Add the posts and pages columns filter. Same function for both.
add_filter('manage_posts_columns', 'pablo_add_thumbnail_column', 2);
add_filter('manage_pages_columns', 'pablo_add_thumbnail_column', 2);
function pablo_add_thumbnail_column($pablo_columns){
  $pablo_columns['pablo_thumb'] = __('Image');
  return $pablo_columns;
}
 
// Add featured image thumbnail to the WP Admin table.
add_action('manage_posts_custom_column', 'pablo_show_thumbnail_column', 5, 2);
add_action('manage_pages_custom_column', 'pablo_show_thumbnail_column', 5, 2);
function pablo_show_thumbnail_column($pablo_columns, $pablo_id){
  switch($pablo_columns){
    case 'pablo_thumb':
    if( function_exists('the_post_thumbnail') )
      echo the_post_thumbnail( 'pablo_admin-featured-image' );
    break;
  }
}

// Move the new column at the first place.
add_filter('manage_posts_columns', 'pablo_column_order');
function pablo_column_order($columns) {
  $n_columns = array();
  $move = 'pablo_thumb'; // which column to move
  $before = 'title'; // move before this column

  foreach($columns as $key => $value) {
    if ($key==$before){
      $n_columns[$move] = $move;
    }
    $n_columns[$key] = $value;
  }
  return $n_columns;
}

// Format the column width with CSS
add_action('admin_head', 'pablo_add_admin_styles');
function pablo_add_admin_styles() {
  echo '<style>.column-pablo_thumb {width: 60px;}</style>';
}

// Get Category & Tag Slugs for Archives
function my_cptui_add_post_types_to_archives( $query ) {
	// We do not want unintended consequences.
	if ( is_admin() || ! $query->is_main_query() ) {
		return;    
	}

	if ( is_category() || is_tag() && empty( $query->query_vars['suppress_filters'] ) ) {
		$cptui_post_types = cptui_get_post_type_slugs();

		$query->set(
			'post_type',
			array_merge(
				array( 'post' ),
				$cptui_post_types
			)
		);
	}
}
add_filter( 'pre_get_posts', 'my_cptui_add_post_types_to_archives' );