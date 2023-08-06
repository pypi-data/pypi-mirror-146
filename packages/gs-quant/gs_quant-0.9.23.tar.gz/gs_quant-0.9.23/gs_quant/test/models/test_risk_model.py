"""
Copyright 2021 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import pytest
from unittest import mock

from gs_quant.models.risk_model import FactorRiskModel
from gs_quant.session import *
from gs_quant.target.risk_models import RiskModel as Risk_Model, RiskModelCoverage, RiskModelTerm,\
    RiskModelUniverseIdentifier, RiskModelType
import datetime as dt


empty_entitlements = {
    "execute": [],
    "edit": [],
    "view": [],
    "admin": [],
    "query": [],
    "upload": []
}

mock_risk_model_obj = Risk_Model(RiskModelCoverage.Country,
                                 'model_id',
                                 'Fake Risk Model',
                                 RiskModelTerm.Long,
                                 RiskModelUniverseIdentifier.gsid,
                                 'GS',
                                 1.0,
                                 entitlements=empty_entitlements,
                                 description='Test',
                                 expected_update_time='00:00:00',
                                 type=RiskModelType.Factor
                                 )


def mock_risk_model(mocker):
    from gs_quant.session import OAuth2Session
    OAuth2Session.init = mock.MagicMock(return_value=None)
    GsSession.use(Environment.QA, 'client_id', 'secret')
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=mock_risk_model_obj)
    mocker.patch.object(GsSession.current, '_get', return_value=mock_risk_model_obj)
    mocker.patch.object(GsSession.current, '_put', return_value=mock_risk_model_obj)
    return FactorRiskModel.get('model_id')


def test_create_risk_model(mocker):
    mock_risk_model(mocker)
    risk_model_id = 'model_id'
    mocker.patch.object(GsSession.current, '_post', return_value=mock_risk_model_obj)
    new_model = FactorRiskModel(risk_model_id,
                                'Fake Risk Model',
                                RiskModelCoverage.Country,
                                RiskModelTerm.Long,
                                RiskModelUniverseIdentifier.gsid,
                                'GS',
                                0.1,
                                entitlements={},
                                description='Test',
                                expected_update_time=dt.datetime.strptime('00:00:00', '%H:%M:%S').time())
    new_model.save()
    assert new_model.id == mock_risk_model_obj.id
    assert new_model.name == mock_risk_model_obj.name
    assert new_model.description == mock_risk_model_obj.description
    assert new_model.term == mock_risk_model_obj.term
    assert new_model.coverage == mock_risk_model_obj.coverage
    assert new_model.universe_identifier == mock_risk_model_obj.universe_identifier
    assert new_model.expected_update_time == dt.datetime.strptime(
        mock_risk_model_obj.expected_update_time, '%H:%M:%S').time()


def test_update_risk_model_entitlements(mocker):
    new_model = mock_risk_model(mocker)
    new_entitlements = {
        "execute": ['guid:X'],
        "edit": [],
        "view": [],
        "admin": [],
        "query": [],
        "upload": []
    }

    new_model.entitlements = new_entitlements
    new_model.save()
    assert 'guid:X' in new_model.entitlements.get('execute')
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    new_model.entitlements = empty_entitlements
    new_model.save()
    new_entitlements = {
        "execute": ['guid:X'],
        "edit": [],
        "view": [],
        "admin": ['guid:XX'],
        "query": [],
        "upload": ['guid:XXX']
    }
    new_model.entitlements = new_entitlements
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert 'guid:X' in new_model.entitlements.get('execute')
    assert 'guid:XX' in new_model.entitlements.get('admin')
    assert 'guid:XXX' in new_model.entitlements.get('upload')


def test_update_risk_model(mocker):
    new_model = mock_risk_model(mocker)

    new_model.term = RiskModelTerm.Short
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.term == RiskModelTerm.Short

    new_model.description = 'Test risk model'
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.description == 'Test risk model'

    new_model.vendor = 'GS'
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.vendor == 'GS'

    new_model.term = RiskModelTerm.Medium
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.term == RiskModelTerm.Medium

    new_model.version = 0.1
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.version == 0.1

    new_model.coverage = RiskModelCoverage.Global
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.coverage == RiskModelCoverage.Global

    new_model.name = 'TEST RISK MODEL'
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.name == 'TEST RISK MODEL'

    new_model.expected_update_time = dt.time(1, 0, 0)
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.expected_update_time == dt.time(1, 0, 0)

    new_model.type = RiskModelType.Thematic
    new_model.save()
    mocker.patch.object(GsSession.current, '_get', return_value=new_model)
    assert new_model.type == RiskModelType.Thematic


if __name__ == "__main__":
    pytest.main([__file__])
