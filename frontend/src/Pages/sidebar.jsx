import React, { useState } from 'react';

export function Sidebar({ onOptionSelect, options }) {
    const [isExpanded, setIsExpanded] = useState(true);

    const toggleSidebar = () => {
        setIsExpanded(!isExpanded);
    };

    return (
        <div className={`sidebar ${isExpanded ? "expanded" : "collapsed"}`}>
            <button className="toggle-btn" onClick={toggleSidebar}>
                {isExpanded ? "<<" : ">>"}
            </button>
            {isExpanded && (
                <ul>
                    {options.map(option => (
                        <li key={option.key} onClick={() => onOptionSelect(option.key)}>
                            {option.label}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
