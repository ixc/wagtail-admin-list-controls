import React, {Component} from "react";
import c from "classnames";

interface TabProps {
    is_selected: boolean;
    on_toggle: () => void;
}

export class Tab extends Component<TabProps, {}> {
    render() {
        const {is_selected, on_toggle} = this.props;
        return (
            <div className={c('alc__tab', {
                'is-selected': is_selected,
            })}>
                <div className="alc__tab__indicator" />
                <button
                    className="button alc__tab__button"
                    type="button"
                    onClick={() => on_toggle()}
                >
                    {this.props.children}
                </button>
            </div>
        );
    }
}
