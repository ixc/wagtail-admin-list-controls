import React from "react";
import {store} from '../state';
import {ListControls} from "./list_controls";
import {Button} from "./button";
import {Panel} from "./panel";
import {Icon} from "./icon";
import {Text} from "./text";
import {Divider} from "./divider";
import {Block} from "./block";
import {Selector} from "./selector";
import {TextFilter} from "./filters/text";

export function Root() {
    const state = store.getState();
    return (
        <div className="alc__root">
            {render_control(state.admin_list_controls)}
        </div>
    );
}

export function render_control(control) {
    switch (control.object_type) {
        case 'list_controls':
            return <ListControls key={control.component_id} control={control}/>;
        case 'button':
            return <Button key={control.component_id} control={control}/>;
        case 'panel':
            return <Panel key={control.component_id} control={control}/>;
        case 'icon':
            return <Icon key={control.component_id} control={control}/>;
        case 'text':
            return <Text key={control.component_id} control={control}/>;
        case 'divider':
            return <Divider key={control.component_id} control={control}/>;
        case 'block':
            return <Block key={control.component_id} control={control}/>;
        case 'selector':
            return <Selector key={control.component_id} control={control}/>;
        case 'filter':
            switch(control.filter_type) {
                case 'text':
                    return <TextFilter key={control.component_id} control={control} />;
                case 'boolean':
                case 'radio':
                case 'choice':
                case 'multiple_choice':
                default:
                    console.error('Unknown filter type', control.filter_type, control);
                    throw new Error(`Unknown filter type "${control.filter_type}`);

            }
        default:
            console.error('Unknown control type', control);
            throw new Error(`Unknown control ${control.object_type}`);
    }
}