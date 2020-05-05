export interface State {
    show_filters: boolean;
    show_sorts: boolean;
    show_reset_button: boolean;
    description: string;
    filtering_options: FilterOptions;
    filter_map: {[name: string]: Filter};
    has_filters: boolean;
    some_filters_have_values: boolean;
    sorting_options: SortOptions;
    sorts: Sort[];
    has_sorts: boolean;
    some_sorts_are_selected: boolean;
    layout_options: LayoutOptions;
    layouts: Layout[];
    has_layouts: boolean;
}

export type FilterOptionChildren = FilterGroup | Filter;

export interface FilterOptions {
    object_type: string;
    children: FilterOptionChildren[];
}

export interface FilterGroup {
    object_type: string;
    title: string;
    children: FilterOptionChildren[];
}

export interface Filter {
    object_type: string;
    type: string;
    value: boolean | string | string[];
    label: string;
    name: string;
    multiple: boolean;
    width: string;
}

export interface SortOptions {
    object_type: string;
    children: Sort[];
}

export interface Sort {
    object_type: string;
    name: string;
    label: string;
    value: string;
    is_selected: boolean;
    results_description: string;
    is_default: boolean;
}

export interface LayoutOptions {
    object_type: string;
    children: Layout[];
}

export interface Layout {
    object_type: string;
    name: string;
    label: string;
    value: string;
    is_selected: boolean;
    icon_class: string;
    template: string;
}

export interface BooleanFilter extends Filter {}

export interface ChoiceFilter extends Filter {
    choices: ChoiceFilterChoice[];
    clearable: boolean;
}

export interface ChoiceFilterChoice {
    value: string;
    label: string;
}

export interface RadioFilter extends Filter {
    choices: RadioFilterChoice[];
}

export interface RadioFilterChoice {
    name: string;
    value: string;
    label: string;
}

export interface StringFilter extends Filter {}
