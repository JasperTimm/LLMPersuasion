import React, { useState } from 'react';
import DemographicsPage from './DemographicsPage';
import PersonalityTraitsPage from './PersonalityTraitsPage';

function UserInfoPage({ setUserInfoCompleted }) {
    const [demographics, setDemographics] = useState(null);

    return (
        <div>
            {!demographics ? (
                <DemographicsPage setDemographics={setDemographics} />
            ) : (
                <PersonalityTraitsPage demographics={demographics} setUserInfoCompleted={setUserInfoCompleted} />
            )}
        </div>
    );
}

export default UserInfoPage;