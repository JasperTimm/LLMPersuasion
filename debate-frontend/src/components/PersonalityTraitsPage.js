import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/UserInfoPage.css';

function PersonalityTraitsPage({ demographics, setUserInfoCompleted }) {
    const [personalityTraits, setPersonalityTraits] = useState({
        extravertedEnthusiastic: '',
        criticalQuarrelsome: '',
        dependableSelfDisciplined: '',
        anxiousEasilyUpset: '',
        openToExperiencesComplex: '',
        reservedQuiet: '',
        sympatheticWarm: '',
        disorganizedCareless: '',
        calmEmotionallyStable: '',
        conventionalUncreative: ''
    });
    const [error, setError] = useState('');

    const handlePersonalityTraitChange = (key, value) => {
        if (value === '' || (value >= 1 && value <= 7)) {
            setPersonalityTraits({
                ...personalityTraits,
                [key]: value
            });
        }
    };

    const isFormValid = () => {
        return Object.values(personalityTraits).every(value => value >= 1 && value <= 7);
    };

    const handleSubmit = async () => {
        if (!isFormValid()) {
            setError('Please fill out all fields with a number between 1 and 7.');
            return;
        }

        try {
            await axiosInstance.post('/user_info', {
                ...demographics,
                ...personalityTraits
            });
            setUserInfoCompleted(true);
        } catch (error) {
            setError('Error submitting user information');
        }
    };

    return (
        <div className="container">
            <h2>Personality Traits</h2>
            <div className="instructions">
                <p>
                    Here are a number of personality traits that may or may not apply to you. 
                    Please write a number next to each statement to indicate the extent to which 
                    you agree or disagree with that statement. You should rate the extent to which 
                    the pair of traits applies to you, even if one characteristic applies more 
                    strongly than the other.
                </p>
                <p>
                    <strong>Rating Scale:</strong>
                </p>
                <ul>
                    <li>1 = Disagree strongly</li>
                    <li>2 = Disagree moderately</li>
                    <li>3 = Disagree a little</li>
                    <li>4 = Neither agree nor disagree</li>
                    <li>5 = Agree a little</li>
                    <li>6 = Agree moderately</li>
                    <li>7 = Agree strongly</li>
                </ul>
                <p><strong>I see myself as:</strong></p>
            </div>
            <input
                type="number"
                min="1"
                max="7"
                value={personalityTraits.extravertedEnthusiastic}
                onChange={(e) => handlePersonalityTraitChange('extravertedEnthusiastic', e.target.value)}
                placeholder="Extraverted, enthusiastic"
            />
            <input
                type="number"
                min="1"
                max="7"
                value={personalityTraits.criticalQuarrelsome}
                onChange={(e) => handlePersonalityTraitChange('criticalQuarrelsome', e.target.value)}
                placeholder="Critical, quarrelsome"
            />
            <input
                type="number"
                min="1"
                max="7"
                value={personalityTraits.dependableSelfDisciplined}
                onChange={(e) => handlePersonalityTraitChange('dependableSelfDisciplined', e.target.value)}
                placeholder="Dependable, self-disciplined"
            />
            <input
                type="number"
                min="1"
                max="7"
                value={personalityTraits.anxiousEasilyUpset}
                onChange={(e) => handlePersonalityTraitChange('anxiousEasilyUpset', e.target.value)}
                placeholder="Anxious, easily upset"
            />
            <input
                type="number"
                min="1"
                max="7"
                value={personalityTraits.openToExperiencesComplex}
                onChange={(e) => handlePersonalityTraitChange('openToExperiencesComplex', e.target.value)}
                placeholder="Open to experiences, complex"
            />
            <input
                type="number"
                min="1"
                max="7"
                value={personalityTraits.reservedQuiet}
                onChange={(e) => handlePersonalityTraitChange('reservedQuiet', e.target.value)}
                placeholder="Reserved, quiet"
            />
            <input
                type="number"
                min="1"
                max="7"
                value={personalityTraits.sympatheticWarm}
                onChange={(e) => handlePersonalityTraitChange('sympatheticWarm', e.target.value)}
                placeholder="Sympathetic, warm"
            />
            <input
                type="number"
                min="1"
                max="7"
                value={personalityTraits.disorganizedCareless}
                onChange={(e) => handlePersonalityTraitChange('disorganizedCareless', e.target.value)}
                placeholder="Disorganized, careless"
            />
            <input
                type="number"
                min="1"
                max="7"
                value={personalityTraits.calmEmotionallyStable}
                onChange={(e) => handlePersonalityTraitChange('calmEmotionallyStable', e.target.value)}
                placeholder="Calm, emotionally stable"
            />
            <input
                type="number"
                min="1"
                max="7"
                value={personalityTraits.conventionalUncreative}
                onChange={(e) => handlePersonalityTraitChange('conventionalUncreative', e.target.value)}
                placeholder="Conventional, uncreative"
            />
            <button onClick={handleSubmit}>Submit</button>
            {error && <p className="error">{error}</p>}
        </div>
    );
}

export default PersonalityTraitsPage;
