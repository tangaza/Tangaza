.. _api:

*************************************
Developer API
*************************************

For use by developers to build applications on top of Nokia Tangaza

.. automodule:: tangaza.Tangaza.api
   :members:
   
   .. function:: login(request)
   
      Returns nothing if login is successful, an error otherwise
      
      .. note:: Method: POST
      
      Example::
      
	Request: http://host/api/login/
		 Params {"username":"some_user", "password":"somepass"}
	Response: ""
	
       
