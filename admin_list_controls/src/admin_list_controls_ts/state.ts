import { createStore } from 'redux';
import immer from "immer";
import _ from "lodash";
import {
    State,
    Filter,
    Sort,
    Layout,
    FilterOptions,
    FilterOptionChildren,
    FilterGroup,
} from "./types";

declare global {
    interface Window {
        admin_list_controls_initial_state: State;
        __REDUX_DEVTOOLS_EXTENSION__: (_: any) => any;
    }
}

export const initial_state = get_initial_state();
export const store = createStore(
    reducer,
    initial_state,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__({
        name: 'admin_list_controls',
    }),
);

export const TOGGLE_FILTER_VISIBILITY = 'TOGGLE_FILTER_VISIBILITY';
export const TOGGLE_SORT_VISIBILITY = 'TOGGLE_SORT_VISIBILITY';
export const HANDLE_FIELD_CHANGE = 'HANDLE_FIELD_CHANGE';
export const SELECT_SORT = 'SELECT_SORT';
export const SELECT_LAYOUT = 'SELECT_LAYOUT';

export interface Action {
    type: string;
}

export interface HandleFieldChangeAction extends Action {
    name: string;
    value: string;
}

export interface SelectSortAction extends Action {
    sort: Sort;
}

export interface SelectLayoutAction extends Action {
    layout: Layout;
}

function reducer(current_state=initial_state, action: Action) {
    return immer(current_state, (state: State) => {
        switch (action.type) {
            case TOGGLE_FILTER_VISIBILITY:
                state.show_filters = !state.show_filters;
                state.show_sorts = false;
                break;
            case TOGGLE_SORT_VISIBILITY:
                state.show_filters = false;
                state.show_sorts = !state.show_sorts;
                break;
            case HANDLE_FIELD_CHANGE:
                const { name, value } = (action as HandleFieldChangeAction);
                const field = state.filter_map[name];
                field.value = value;
                break;
            case SELECT_SORT:
                const { sort } = (action as SelectSortAction);
                state.sorts.forEach(sort => {
                    sort.is_selected = false;
                });
                sort.is_selected = true;
                break;
            case SELECT_LAYOUT:
                const { layout } = (action as SelectLayoutAction);
                state.layouts.forEach(layout => {
                    layout.is_selected = false;
                });
                layout.is_selected = true;
                break;
            default:
                break;
        }
    });
}

function get_initial_state(): State {
    if (!window.admin_list_controls_initial_state) {
        throw new Error('Global `admin_list_controls_initial_state` has not been defined');
    }

    const initial_state = _.assign({}, window.admin_list_controls_initial_state);

    // Normalize the filter data
    initial_state.filter_map = {};
    const filter_options = initial_state.filtering_options;
    const filters = filter_options ? get_filters_from_options(filter_options) : [];
    filters.forEach(obj => {
        initial_state.filter_map[obj.name] = obj;
    });
    initial_state.has_filters = filters.length > 0;
    initial_state.some_filters_have_values = _.some(filters, obj => {
        if (obj.multiple) {
            return !!(obj.value as []).length;
        } else {
            return !!obj.value;
        }
    });

    // Normalize the sort data
    const sort_options = initial_state.sorting_options;
    initial_state.sorts = sort_options ? sort_options.children : [];
    initial_state.has_sorts = initial_state.sorts.length > 0;
    initial_state.some_sorts_are_selected = _.some(initial_state.sorts, sort => {
        return sort.is_selected && !sort.is_default;
    });

    // Normalize the layout data
    const layout_options = initial_state.layout_options;
    initial_state.layouts = layout_options
        ? initial_state.layout_options.children
        : [];
    initial_state.has_layouts = initial_state.layouts.length > 0;

    return initial_state;
}

function get_filters_from_options(options: FilterOptions): Filter[] {
    return _traverse_and_find_filters(options.children, []);
}

function _traverse_and_find_filters(root: FilterOptionChildren[], accum: Filter[]) {
    root.forEach(obj => {
        if (obj.object_type === 'filter') {
            accum.push(obj as Filter);
        } else {
            _traverse_and_find_filters(
                (obj as FilterGroup).children,
                accum,
            );
        }
    });

    return accum
}
