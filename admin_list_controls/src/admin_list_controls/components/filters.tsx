import React, {Component} from "react";
import c from 'classnames';
import { store } from '../state';
import { ChoiceField} from './fields/choice_field';
import { StringField } from './fields/string_field';
import { BooleanField } from "./fields/boolean_field";
import { RadioField } from "./fields/radio_field";
import { TabContent } from "./tab_content";
import { submit_search } from '..';
import * as types from '../types';

export class Filters extends Component<{}, {}> {
    render() {
        const state: types.State = store.getState();

        if (!state.has_filters) {
            return null;
        }

        return (
            <TabContent show_content={state.show_filters}>
                {/* A form element allows for keyboards to trigger submit events (enter keypress, etc) */}
                <form onSubmit={event => {
                    event.preventDefault();
                    submit_search();
                }}>
                    <div className="alc__filter__children">
                        {state.filtering_options.children.map((obj, i) => render_filter_object(obj, i))}
                    </div>
                    <div className="alc__filter__buttons">
                        <button
                            className="button alc__filter__submit"
                            type="submit"
                            onClick={submit_search}
                        >
                            <i className="icon-fa icon-fa-search" />
                            Apply filters
                        </button>
                    </div>
                </form>
            </TabContent>
        );
    }
}

function render_filter_object(obj: types.FilterOptionChildren, key: number) {
    if (obj.object_type === 'filter_group') {
        return <FilterGroup key={key} obj={obj as types.FilterGroup} />;
    } else if (obj.object_type === 'filter') {
        return <Filter key={key} obj={obj as types.Filter} />;
    } else {
        throw new Error(`Unknown object_type ${obj.object_type} in ${JSON.stringify(obj)}`);
    }
}

function FilterGroup(props: {obj: types.FilterGroup}) {
    const {obj} = props;

    return (
        <div className="alc__filter__group">
            {obj.title
                ? <div className="alc__filter__group__title">{obj.title}</div>
                : null
            }
            <div className="alc__filter__group__children">
                {obj.children.map((obj, i) => render_filter_object(obj, i))}
            </div>
        </div>
    );
}

function Filter(props: {obj: types.Filter}) {
    const {obj} = props;
    const state: types.State = store.getState();
    const filter = state.filter_map[obj.name];

    let rendered_field;
    if (filter.type === 'string') {
        rendered_field = <StringField field={filter as types.StringFilter} />;
    } else if (filter.type === 'choice') {
        rendered_field = <ChoiceField field={filter as types.ChoiceFilter} />;
    } else if (filter.type === 'boolean') {
        rendered_field = <BooleanField field={filter as types.BooleanFilter} />;
    } else if (filter.type === 'radio') {
        rendered_field = <RadioField field={filter as types.RadioFilter} />;
    } else {
        throw new Error(`Unknown filter type ${filter.type} in ${JSON.stringify(filter)}`);
    }

    return (
        <div className={c('alc__filter__field', {
            'alc__filter__field--half-width': filter.width === 'half_width',
            'alc__filter__field--full-width': filter.width === 'full_width',
        })}>{rendered_field}</div>
    );
}
