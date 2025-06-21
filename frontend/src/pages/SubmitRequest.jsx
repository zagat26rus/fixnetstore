import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Textarea } from '../components/ui/textarea';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Checkbox } from '../components/ui/checkbox';
import { useToast } from '../hooks/use-toast';
import { deviceTypes, issueTypes } from '../mock/data';
import { repairAPI } from '../services/api';

const SubmitRequest = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    customerName: '',
    customerEmail: '',
    customerPhone: '',
    deviceBrand: '',
    deviceModel: '',
    issueCategory: '',
    specificIssue: '',
    description: '',
    urgency: 'normal',
    pickupAddress: '',
    pickupTime: '',
    gdprConsent: false
  });

  const [currentStep, setCurrentStep] = useState(1);
  const [availableModels, setAvailableModels] = useState([]);
  const [availableIssues, setAvailableIssues] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleDeviceBrandChange = (brand) => {
    setFormData(prev => ({ ...prev, deviceBrand: brand, deviceModel: '' }));
    const selectedBrand = deviceTypes.find(d => d.name === brand);
    setAvailableModels(selectedBrand ? selectedBrand.models : []);
  };

  const handleIssueCategoryChange = (category) => {
    setFormData(prev => ({ ...prev, issueCategory: category, specificIssue: '' }));
    const selectedCategory = issueTypes.find(i => i.category === category);
    setAvailableIssues(selectedCategory ? selectedCategory.issues : []);
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.gdprConsent) {
      toast({
        title: "Privacy Consent Required",
        description: "Please accept our privacy policy to continue.",
        variant: "destructive"
      });
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await repairAPI.createRequest(formData);
      
      if (response.success) {
        toast({
          title: "Repair Request Submitted!",
          description: `Your ticket ID is ${response.ticket_id}. We'll contact you within 2 hours.`,
        });

        // Reset form
        setFormData({
          customerName: '',
          customerEmail: '',
          customerPhone: '',
          deviceBrand: '',
          deviceModel: '',
          issueCategory: '',
          specificIssue: '',
          description: '',
          urgency: 'normal',
          pickupAddress: '',
          pickupTime: '',
          gdprConsent: false
        });
        setCurrentStep(1);
      } else {
        throw new Error(response.message || 'Failed to submit request');
      }
    } catch (error) {
      console.error('Submission error:', error);
      toast({
        title: "Submission Failed",
        description: error.response?.data?.detail || error.message || "Please try again later.",
        variant: "destructive"
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const nextStep = () => {
    if (currentStep < 3) setCurrentStep(currentStep + 1);
  };

  const prevStep = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
  };

  const isStepValid = () => {
    switch (currentStep) {
      case 1:
        return formData.deviceBrand && formData.deviceModel && formData.issueCategory && formData.specificIssue;
      case 2:
        return formData.customerName && formData.customerEmail && formData.customerPhone;
      case 3:
        return formData.pickupAddress && formData.gdprConsent;
      default:
        return false;
    }
  };

  return (
    <div className="min-h-screen pt-20 bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Submit Repair
            <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Request
            </span>
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Tell us about your device issue and we'll get you a repair quote within 2 hours.
          </p>
        </div>

        {/* Progress Indicator */}
        <div className="mb-12">
          <div className="flex items-center justify-center space-x-8">
            {[1, 2, 3].map((step) => (
              <div key={step} className="flex items-center">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center font-semibold transition-all duration-300 ${
                  currentStep >= step 
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg' 
                    : 'bg-gray-200 text-gray-500'
                }`}>
                  {step}
                </div>
                {step < 3 && (
                  <div className={`w-16 h-1 mx-4 transition-all duration-300 ${
                    currentStep > step ? 'bg-gradient-to-r from-blue-600 to-purple-600' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-center mt-4 space-x-16 text-sm font-medium text-gray-600">
            <span className={currentStep >= 1 ? 'text-blue-600' : ''}>Device Info</span>
            <span className={currentStep >= 2 ? 'text-blue-600' : ''}>Contact Details</span>
            <span className={currentStep >= 3 ? 'text-blue-600' : ''}>Pickup & Consent</span>
          </div>
        </div>

        <Card className="shadow-2xl border-0 bg-white/80 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-2xl font-bold text-center">
              {currentStep === 1 && "Tell us about your device"}
              {currentStep === 2 && "Your contact information"}
              {currentStep === 3 && "Pickup details & consent"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Step 1: Device Information */}
              {currentStep === 1 && (
                <div className="space-y-6 animate-fade-in">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label className="text-sm font-medium text-gray-700">Device Brand</Label>
                      <Select value={formData.deviceBrand} onValueChange={handleDeviceBrandChange}>
                        <SelectTrigger className="mt-2">
                          <SelectValue placeholder="Select your device brand" />
                        </SelectTrigger>
                        <SelectContent>
                          {deviceTypes.map((device) => (
                            <SelectItem key={device.name} value={device.name}>
                              {device.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label className="text-sm font-medium text-gray-700">Device Model</Label>
                      <Select 
                        value={formData.deviceModel} 
                        onValueChange={(value) => handleInputChange('deviceModel', value)}
                        disabled={!formData.deviceBrand}
                      >
                        <SelectTrigger className="mt-2">
                          <SelectValue placeholder="Select your device model" />
                        </SelectTrigger>
                        <SelectContent>
                          {availableModels.map((model) => (
                            <SelectItem key={model} value={model}>
                              {model}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label className="text-sm font-medium text-gray-700">Issue Category</Label>
                      <Select value={formData.issueCategory} onValueChange={handleIssueCategoryChange}>
                        <SelectTrigger className="mt-2">
                          <SelectValue placeholder="What type of issue?" />
                        </SelectTrigger>
                        <SelectContent>
                          {issueTypes.map((issue) => (
                            <SelectItem key={issue.category} value={issue.category}>
                              {issue.category}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label className="text-sm font-medium text-gray-700">Specific Issue</Label>
                      <Select 
                        value={formData.specificIssue} 
                        onValueChange={(value) => handleInputChange('specificIssue', value)}
                        disabled={!formData.issueCategory}
                      >
                        <SelectTrigger className="mt-2">
                          <SelectValue placeholder="Select specific issue" />
                        </SelectTrigger>
                        <SelectContent>
                          {availableIssues.map((issue) => (
                            <SelectItem key={issue} value={issue}>
                              {issue}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-gray-700">Describe the Issue</Label>
                    <Textarea
                      value={formData.description}
                      onChange={(e) => handleInputChange('description', e.target.value)}
                      placeholder="Please provide more details about the issue..."
                      className="mt-2 min-h-[120px]"
                    />
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-gray-700">Urgency Level</Label>
                    <Select value={formData.urgency} onValueChange={(value) => handleInputChange('urgency', value)}>
                      <SelectTrigger className="mt-2">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="normal">Normal (2-3 days)</SelectItem>
                        <SelectItem value="urgent">Urgent (24 hours)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              )}

              {/* Step 2: Contact Information */}
              {currentStep === 2 && (
                <div className="space-y-6 animate-fade-in">
                  <div>
                    <Label className="text-sm font-medium text-gray-700">Full Name</Label>
                    <Input
                      value={formData.customerName}
                      onChange={(e) => handleInputChange('customerName', e.target.value)}
                      placeholder="Enter your full name"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-gray-700">Email Address</Label>
                    <Input
                      type="email"
                      value={formData.customerEmail}
                      onChange={(e) => handleInputChange('customerEmail', e.target.value)}
                      placeholder="Enter your email address"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-gray-700">Phone Number</Label>
                    <Input
                      type="tel"
                      value={formData.customerPhone}
                      onChange={(e) => handleInputChange('customerPhone', e.target.value)}
                      placeholder="Enter your phone number"
                      className="mt-2"
                    />
                  </div>
                </div>
              )}

              {/* Step 3: Pickup & Consent */}
              {currentStep === 3 && (
                <div className="space-y-6 animate-fade-in">
                  <div>
                    <Label className="text-sm font-medium text-gray-700">Pickup Address</Label>
                    <Textarea
                      value={formData.pickupAddress}
                      onChange={(e) => handleInputChange('pickupAddress', e.target.value)}
                      placeholder="Enter your full address for device pickup"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label className="text-sm font-medium text-gray-700">Preferred Pickup Time</Label>
                    <Select value={formData.pickupTime} onValueChange={(value) => handleInputChange('pickupTime', value)}>
                      <SelectTrigger className="mt-2">
                        <SelectValue placeholder="Select preferred time" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="9am-12pm">9:00 AM - 12:00 PM</SelectItem>
                        <SelectItem value="12pm-3pm">12:00 PM - 3:00 PM</SelectItem>
                        <SelectItem value="3pm-6pm">3:00 PM - 6:00 PM</SelectItem>
                        <SelectItem value="flexible">Flexible</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-start space-x-3 p-4 bg-blue-50 rounded-lg">
                    <Checkbox
                      id="gdpr"
                      checked={formData.gdprConsent}
                      onCheckedChange={(checked) => handleInputChange('gdprConsent', checked)}
                    />
                    <div className="text-sm">
                      <label htmlFor="gdpr" className="font-medium text-gray-700 cursor-pointer">
                        I consent to data processing
                      </label>
                      <p className="text-gray-600 mt-1">
                        I agree to FixNet processing my personal data for repair services as outlined in the Privacy Policy. 
                        Your data will only be used for repair coordination and will not be shared with third parties.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Navigation Buttons */}
              <div className="flex justify-between pt-6">
                <Button
                  type="button"
                  onClick={prevStep}
                  variant="outline"
                  disabled={currentStep === 1 || isSubmitting}
                  className="px-8 py-3"
                >
                  Previous
                </Button>

                {currentStep < 3 ? (
                  <Button
                    type="button"
                    onClick={nextStep}
                    disabled={!isStepValid() || isSubmitting}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-8 py-3"
                  >
                    Next Step
                  </Button>
                ) : (
                  <Button
                    type="submit"
                    disabled={!isStepValid() || isSubmitting}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-8 py-3"
                  >
                    {isSubmitting ? (
                      <div className="flex items-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        Submitting...
                      </div>
                    ) : (
                      'Submit Request'
                    )}
                  </Button>
                )}
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default SubmitRequest;