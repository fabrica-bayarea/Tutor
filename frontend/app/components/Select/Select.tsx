'use client';

import ReactSelect, { StylesConfig, GroupBase } from 'react-select';

export type SelectOption<V = string> = { value: V; label: string };

type SelectProps<V = string> = {
    options: SelectOption<V>[];
    value?: SelectOption<V> | SelectOption<V>[] | null;
    onChange: (value: SelectOption<V> | SelectOption<V>[] | null) => void;
    placeholder?: string;
    isMulti?: boolean;
    isSearchable?: boolean;
    isDisabled?: boolean;
    instanceId?: string;
    getOptionValue?: (option: SelectOption<V>) => string;
    className?: string;
};

function buildStyles<V>(): StylesConfig<SelectOption<V>, boolean, GroupBase<SelectOption<V>>> {
    return {
        control: (base, state) => ({
            ...base,
            minHeight: '40px',
            borderRadius: '8px',
            borderColor: state.isFocused ? '#0d9488' : '#e5e5e5',
            backgroundColor: state.isDisabled ? '#f2f2f2' : '#ffffff',
            boxShadow: 'none',
            opacity: state.isDisabled ? 0.7 : 1,
            transition: 'border-color 0.15s ease',
            '&:hover': {
                borderColor: state.isFocused ? '#0d9488' : 'rgba(0,0,0,0.3)',
            },
        }),
        placeholder: (base) => ({
            ...base,
            color: '#999999',
            fontSize: '14px',
        }),
        input: (base) => ({
            ...base,
            color: '#262626',
            fontSize: '14px',
        }),
        singleValue: (base) => ({
            ...base,
            color: '#262626',
            fontSize: '14px',
        }),
        option: (base, state) => ({
            ...base,
            fontSize: '14px',
            backgroundColor: state.isSelected
                ? '#f0fdfa'
                : state.isFocused
                ? 'rgba(13,148,136,0.08)'
                : 'transparent',
            color: state.isSelected ? '#0f766e' : '#262626',
            fontWeight: state.isSelected ? 500 : 400,
            cursor: 'pointer',
            '&:active': {
                backgroundColor: 'rgba(13,148,136,0.15)',
            },
        }),
        menu: (base) => ({
            ...base,
            borderRadius: '8px',
            border: '1px solid #e5e5e5',
            boxShadow: '0 4px 16px rgba(0,0,0,0.10)',
            marginTop: '4px',
        }),
        menuList: (base) => ({
            ...base,
            padding: '4px',
        }),
        multiValue: (base) => ({
            ...base,
            backgroundColor: '#f0fdfa',
            border: '1px solid #14b8a6',
            borderRadius: '6px',
        }),
        multiValueLabel: (base) => ({
            ...base,
            color: '#0f766e',
            fontSize: '13px',
            fontWeight: 500,
        }),
        multiValueRemove: (base) => ({
            ...base,
            color: '#0f766e',
            borderRadius: '0 6px 6px 0',
            '&:hover': {
                backgroundColor: '#0d9488',
                color: '#ffffff',
            },
        }),
        indicatorSeparator: (base) => ({
            ...base,
            backgroundColor: '#e5e5e5',
        }),
        dropdownIndicator: (base) => ({
            ...base,
            color: '#737373',
            '&:hover': { color: '#262626' },
        }),
        clearIndicator: (base) => ({
            ...base,
            color: '#737373',
            '&:hover': { color: '#dc2626' },
        }),
    };
}

export default function Select<V = string>({
    options,
    value,
    onChange,
    placeholder = 'Selecione...',
    isMulti = false,
    isSearchable = true,
    isDisabled = false,
    instanceId,
    getOptionValue,
    className,
}: SelectProps<V>) {
    const styles = buildStyles<V>();

    return (
        <ReactSelect
            instanceId={instanceId}
            options={options}
            value={value}
            onChange={onChange as any}
            placeholder={placeholder}
            isMulti={isMulti}
            isSearchable={isSearchable}
            isDisabled={isDisabled}
            styles={styles}
            className={className}
            getOptionValue={getOptionValue as any}
            noOptionsMessage={() => 'Nenhuma opção encontrada'}
        />
    );
}
