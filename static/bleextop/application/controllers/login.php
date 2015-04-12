<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
/**
 * CodeIgniter
 *
 * An open source application development framework for PHP 5.1.6 or newer
 *
 * @package		CodeIgniter
 * @author		ExpressionEngine Dev Team
 * @copyright	Copyright (c) 2008 - 2011, EllisLab, Inc.
 * @license		http://codeigniter.com/user_guide/license.html
 * @link		http://codeigniter.com
 * @since		Version 1.0
 * @filesource
 */

// ------------------------------------------------------------------------

/**
 * CodeIgniter Application Controller Class
 *
 * This class object is the super class that every library in
 * CodeIgniter will be assigned to.
 *
 * @package		CodeIgniter
 * @subpackage	Libraries
 * @category	Libraries
 * @author		ExpressionEngine Dev Team
 * @link		http://codeigniter.com/user_guide/general/controllers.html
 */
class CI_Controller {
	
	/*Moose added for CI code completion in IDE*/
	/**
	 * @var CI_Config
	 */
	var $config;
	/**
	 * @var CI_DB_active_record
	 */
	var $db;
	/**
	 * @var CI_Email
	 */
	var $email;
	/**
	 * @var CI_Form_validation
	 */
	var $form_validation;
	/**
	 * @var CI_Input
	 */
	var $input;
	/**
	 * @var CI_Loader
	 */
	var $load;
	/**
	 * @var CI_Router
	 */
	var $router;
	/**
	 * @var CI_Session
	 */
	var $session;
	/**
	 * @var CI_Table
	 */
	var $table;
	/**
	 * @var CI_Unit_test
	 */
	var $unit;
	/**
	 * @var CI_URI
	 */
	var $uri;
	/**
	 * @var CI_Pagination
	 */
	var $pagination;
	
	/*Moose added for FB code completion in IDE*/
	/**
	 * @var Facebook
	 */
	var $facebook;
	
	private static $instance;

	/**
	 * Constructor
	 */
	public function __construct()
	{
		self::$instance =& $this;
		
		// Assign all the class objects that were instantiated by the
		// bootstrap file (CodeIgniter.php) to local class variables
		// so that CI can run as one big super object.
		foreach (is_loaded() as $var => $class)
		{
			$this->$var =& load_class($class);
		}

		$this->load =& load_class('Loader', 'core');

		$this->load->initialize();
		
		log_message('debug', "Controller Class Initialized");
	}

	public static function &get_instance()
	{
		return self::$instance;
	}
}


class Login extends CI_Controller{
	
	function index(){
		$this->load->view("welcome");
	}
	
	function logout(){
		$this->session->sess_destroy();
		$this->index();
	}
	
	function validate(){
		$this->load->model("userdao");
		
		$data = array(
			"username"	=> $this->input->post("username"),
			"password"	=> md5($this->input->post("password"))
		);
		
		$isValid = $this->userdao->validate($data);
		
		if($isValid){
			$user = $this->userdao->getUser($data);
			unset($user["password"]);
			
			$this->session->set_userdata(array(
				"user"			=> $user,
				"is_logged_in"	=> true
			));
			
			echo json_encode(array(
				"success"	=> true,
				"url"		=> "static/bleextop/application/controllers/desktop/home"
			));
		}else{
			echo json_encode(array(
				"success"	=> false,
				"message"	=> "Wrong credentials"
			));
		}
	}
	
}