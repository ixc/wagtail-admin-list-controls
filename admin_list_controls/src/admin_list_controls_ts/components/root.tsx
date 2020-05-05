import React, {Component} from "react";
import c from 'classnames';
import { Filters } from './filters';
import { Sorts } from './sorts';
import { Layouts } from './layouts';
import { Reset } from './reset';
import { Tab } from './tab';
import { TextualDescription } from './textual_description';
import { store, TOGGLE_FILTER_VISIBILITY, TOGGLE_SORT_VISIBILITY } from '../state';
import { State } from '../types';


export class Root extends Component<{}, {}> {
    render() {
        const state: State = store.getState();
        return (
            <div className={c('alc__root', {
                'has-description': state.description,
                'has-no-description': !state.description,
            })}>
                <div className="alc__tab-list clearfix">
                    {state.has_filters
                        ? (
                            <Tab
                                is_selected={state.show_filters}
                                on_toggle={() => store.dispatch({ type: TOGGLE_FILTER_VISIBILITY })}
                            >
                                <i className="icon-fa icon-fa-search-plus" />
                                Advanced search
                            </Tab>
                        )
                        : null
                    }
                    {state.has_sorts
                        ? (
                            <Tab
                                is_selected={state.show_sorts}
                                on_toggle={() => store.dispatch({ type: TOGGLE_SORT_VISIBILITY })}
                            >
                                <i className="icon-fa icon-fa-sort-amount-desc" />
                                Order results
                            </Tab>
                        )
                        : null
                    }
                    <Reset />
                    <Layouts />
                </div>
                <div>
                    <Filters />
                    <Sorts />
                </div>
                <div className="alc__root__description">
                    <TextualDescription />
                </div>
            </div>
        );
    }
}
