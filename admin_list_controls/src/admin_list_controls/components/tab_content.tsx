import React, {Component} from "react";

interface TabContentProps {
    show_content: boolean;
}

export class TabContent extends Component<TabContentProps, {}> {
    render() {
        const {show_content, children} = this.props;

        return (
            <div
                className="alc__tab-content"
                style={{display: show_content ? 'block': 'none'}}
            >
                <div className="alc__tab-content__inner">
                    {children}
                </div>
            </div>
        );
    }
}
