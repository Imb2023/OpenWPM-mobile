from automation import TaskManager, CommandSequence
from tld import get_tld

# The list of sites that we wish to crawl
NUM_BROWSERS = 15
# sites = ["https://securehomes.esat.kuleuven.be/~gacar/dev/test/sensor/"]
sites = []
csv_name = "top-1m.csv"
no_of_sites = 100000
for l in open(csv_name).readlines()[1:no_of_sites]:
    url = l.split(",")[-1].rstrip()
    sites.append("http://%s" % url)
#sites = ['http://www.example.com',
         #'http://www.princeton.edu',
         #'http://citp.princeton.edu/']

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in xrange(NUM_BROWSERS):
    browser_params[i]['http_instrument'] = True  # Record HTTP Requests and Responses
    browser_params[i]['disable_flash'] = True  # Disable flash for all three browsers
    browser_params[i]['js_instrument'] = True  # Enable JS instrumentation
    browser_params[i]['cp_instrument'] = True  # Enable content policy instrumentation
    browser_params[i]['save_javascript'] = True  # save JS files
    browser_params[i]['headless'] = True  #Launch only browser 0 headless

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/openwpm/'
manager_params['log_directory'] = '~/openwpm/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
for site in sites:
    command_sequence = CommandSequence.CommandSequence(site, reset=True)

    # Start by visiting the page
    command_sequence.get(sleep=10, timeout=60)
    command_sequence.save_screenshot(get_tld(site) + '_screenshot')
    # dump_profile_cookies/dump_flash_cookies closes the current tab.
    command_sequence.dump_profile_cookies(120)

    manager.execute_command_sequence(command_sequence) # ** = synchronized browsers

# Shuts down the browsers and waits for the data to finish logging
manager.close()
